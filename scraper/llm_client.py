"""Resilient LLM client wrapper with retry logic for free-tier models.

Free models on OpenRouter may return empty responses or rate-limit errors.
This wrapper retries with exponential backoff.
"""
import os
import sys
import time
from typing import List, Optional

from openai import OpenAI

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

DEFAULT_MODEL = "qwen/qwen3-coder-next"
MAX_RETRIES = 4
BASE_DELAY = 3.0
MAX_DELAY = 30.0


class ResilientLLMClient:
    def __init__(self, model: str = DEFAULT_MODEL, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model
        self.client: Optional[OpenAI] = None
        if self.api_key:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
            )

    @property
    def available(self) -> bool:
        return self.client is not None

    def chat(
        self,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 2000,
        system: Optional[str] = None,
    ) -> Optional[str]:
        """Send a chat completion request with retry logic.

        Returns the response text, or None if all retries fail.
        """
        if not self.client:
            return None

        messages: List[dict] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        for attempt in range(MAX_RETRIES + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                raw = response.choices[0].message.content
                finish_reason = getattr(response.choices[0], "finish_reason", "unknown")

                if raw and raw.strip():
                    if attempt > 0:
                        print(f"  [llm] Success on attempt {attempt + 1}", file=sys.stderr)
                    return raw.strip()

                # Empty response
                print(f"  [llm] Empty response (attempt {attempt + 1}/{MAX_RETRIES + 1}, finish_reason={finish_reason})", file=sys.stderr)

            except Exception as e:
                error_str = str(e)
                print(f"  [llm] Error (attempt {attempt + 1}/{MAX_RETRIES + 1}): {error_str[:120]}", file=sys.stderr)

                if "rate" in error_str.lower() or "429" in error_str:
                    pass  # will retry with backoff
                elif attempt >= MAX_RETRIES:
                    return None

            if attempt < MAX_RETRIES:
                delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)
                print(f"  [llm] Retrying in {delay:.0f}s...", file=sys.stderr)
                time.sleep(delay)

        print(f"  [llm] All {MAX_RETRIES + 1} attempts failed", file=sys.stderr)
        return None
