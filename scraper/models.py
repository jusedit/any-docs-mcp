"""Pydantic models for the scraper pipeline."""
from __future__ import annotations

import re
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class EngineMode(str, Enum):
    CURL = "curl"
    SELENIUM = "selenium"


class EngineDecision(BaseModel):
    mode: EngineMode
    curl_md_length: int = 0
    selenium_md_length: int = 0
    curl_headings: int = 0
    selenium_headings: int = 0
    curl_code_blocks: int = 0
    selenium_code_blocks: int = 0
    diff_ratio: float = 0.0
    reason: str = ""


class ScopeRules(BaseModel):
    include_patterns: List[str] = Field(default_factory=list)
    exclude_patterns: List[str] = Field(default_factory=list)
    base_url: str = ""
    description: str = ""

    @staticmethod
    def _anchor_pattern(pat: str) -> str:
        """Anchor simple path patterns so /ru doesn't match /rules.

        If the pattern looks like a plain path segment (e.g. /ru, /blog, /docs/),
        anchor it so it only matches as a complete path segment.
        Patterns that already contain regex metacharacters are left as-is.
        """
        # Already a regex (has metacharacters beyond /)
        if re.search(r'[\\^$*+?{}()\[\]|.]', pat):
            return pat
        # Simple path like /ru or /docs/ — anchor as segment boundary
        # /ru should match /ru and /ru/... but NOT /rules
        stripped = pat.rstrip('/')
        return f"(?:^|/){re.escape(stripped.lstrip('/'))}(?:/|$)"

    def url_matches(self, url: str) -> bool:
        if not url.startswith(self.base_url):
            return False
        # Extract path for matching — LLMs return path-based patterns like /docs/
        from urllib.parse import urlparse
        path = urlparse(url).path
        for pat in self.exclude_patterns:
            anchored = self._anchor_pattern(pat)
            try:
                if re.search(anchored, path, re.IGNORECASE):
                    return False
            except re.error:
                continue
        if self.include_patterns:
            for pat in self.include_patterns:
                anchored = self._anchor_pattern(pat)
                try:
                    if re.search(anchored, path, re.IGNORECASE):
                        return True
                except re.error:
                    continue
            return False
        return True


class SelectorSpec(BaseModel):
    content_selector: str = "main"
    prune_selectors: List[str] = Field(default_factory=list)
    notes: str = ""


class LLMAnalysis(BaseModel):
    scope_rules: ScopeRules
    selector_spec: SelectorSpec


class UrlRecord(BaseModel):
    url: str
    title: str = ""
    discovered_from: str = ""
    source: str = ""
    depth: int = 0


class ManifestEntry(BaseModel):
    url: str
    md_raw_path: str
    size_bytes: int = 0
    headings: List[str] = Field(default_factory=list)
    content_hash: str = ""


class Manifest(BaseModel):
    start_url: str
    engine_mode: str = "curl"
    total_pages: int = 0
    total_files: int = 0
    entries: List[ManifestEntry] = Field(default_factory=list)


class GroupPlanEntry(BaseModel):
    name: str
    paths: List[str] = Field(default_factory=list)
    output_path: str = ""
    rationale: str = ""


class GroupPlan(BaseModel):
    groups: List[GroupPlanEntry] = Field(default_factory=list)


class PipelineConfig(BaseModel):
    start_url: str
    name: str
    output_dir: str = "./output"
    max_pages: int = 500
    max_workers: int = 10
    engine_diff_threshold: float = 0.3
    max_file_size_kb: int = 500
    llm_model_analyzer: str = "qwen/qwen3-coder-next"
