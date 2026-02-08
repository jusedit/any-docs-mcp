"""FR3: LLM Analyzer — URL filter rules + CSS selectors via OpenRouter / Haiku 4.5.

Input:
  - Start page HTML (or MD preview)
  - ~10 sample pages (HTML/MD preview)
  - Discovered URL list (truncated)

Output (strict JSON):
  - include_patterns[] (regex)
  - exclude_patterns[] (regex)
  - content_selector (CSS)
  - prune_selectors[] (CSS)
  - notes (debug)

Falls back to safe defaults when LLM is unavailable or returns invalid JSON.
Includes retry loop with feedback when scope validation fails.
"""
import json
import os
import re
import sys
from collections import defaultdict
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from llm_client import ResilientLLMClient
from models import LLMAnalysis, ScopeRules, SelectorSpec


FALLBACK_CONTENT_SELECTORS = ["main", "article", ".content", "#content", ".documentation"]
FALLBACK_PRUNE_SELECTORS = [
    "nav", "header", "footer", ".cookie-banner", ".newsletter",
    ".feedback", ".edit-page", ".breadcrumb", ".toc",
]

MAX_LLM_RETRIES = 2


class LLMAnalyzer:
    def __init__(self, model: str = "qwen/qwen3-coder-next", api_key: Optional[str] = None):
        self.model = model
        self.llm = ResilientLLMClient(model=model, api_key=api_key)
        self.client = self.llm.client  # for backward compat checks

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def analyze(
        self,
        start_url: str,
        base_url: str,
        start_html: str,
        sample_links: Set[str],
        sample_htmls: Optional[List[str]] = None,
    ) -> LLMAnalysis:
        """Run LLM analysis to get scope rules + selector spec.

        Includes retry loop: if scope validation fails, retries with feedback.
        Falls back to heuristic defaults if LLM unavailable or all retries fail.
        """
        if not self.llm.available:
            print("  [llm-analyzer] No API key — using heuristic fallback", file=sys.stderr)
            return self._fallback(start_url, base_url, start_html)

        try:
            return self._llm_analyze_with_retry(
                start_url, base_url, start_html, sample_links, sample_htmls
            )
        except Exception as e:
            print(f"  [llm-analyzer] LLM call failed: {e} — using fallback", file=sys.stderr)
            return self._fallback(start_url, base_url, start_html)

    def reanalyze_selectors(
        self,
        start_url: str,
        base_url: str,
        start_html: str,
        previous_selector: str,
        crawl_success_rate: float,
        total_pages: int,
        sample_links: Set[str],
    ) -> LLMAnalysis:
        """Re-analyze with feedback about poor crawl results.

        Called by pipeline when crawl quality is below threshold.
        """
        if not self.llm.available:
            return self._fallback(start_url, base_url, start_html)

        print(f"  [llm-analyzer] Re-analyzing with crawl feedback (success rate: {crawl_success_rate:.1%})", file=sys.stderr)

        feedback = (
            f"IMPORTANT FEEDBACK: A previous crawl attempt using content_selector='{previous_selector}' "
            f"only extracted content from {crawl_success_rate:.0%} of {total_pages} pages. "
            f"The selector is likely wrong. Please analyze the HTML more carefully and provide "
            f"a content_selector that actually matches the main content area on this site."
        )

        return self._llm_analyze(
            start_url, base_url, start_html, sample_links,
            extra_context=feedback,
        )

    def refine_selectors(
        self,
        current_analysis: LLMAnalysis,
        sample_md_contents: List[str],
        start_url: str,
        start_html: str,
    ) -> SelectorSpec:
        """Refine prune selectors by showing the LLM actual crawl output.

        The LLM sees 2-3 sample markdown pages and identifies repeated
        UI residue that should be pruned with better CSS selectors.
        Returns an improved SelectorSpec.
        """
        if not self.llm.available or not sample_md_contents:
            return current_analysis.selector_spec

        print(f"  [llm-refine] Refining selectors with {len(sample_md_contents)} sample pages...", file=sys.stderr)

        # Show first ~1500 chars of each sample
        samples_text = ""
        for i, content in enumerate(sample_md_contents[:3]):
            preview = content[:1500]
            samples_text += f"\n\n--- SAMPLE PAGE {i+1} (first 1500 chars) ---\n{preview}\n"

        clean_html = self._sanitize_html(start_html)

        prompt = f"""You previously analyzed a documentation site and chose these CSS selectors:
- content_selector: {current_analysis.selector_spec.content_selector}
- prune_selectors: {json.dumps(current_analysis.selector_spec.prune_selectors)}

Here is the ORIGINAL HTML of the start page (truncated):
```html
{clean_html[:8000]}
```

Here is the ACTUAL MARKDOWN OUTPUT from crawling several pages with your selectors:
{samples_text}

PROBLEM: The markdown output still contains UI artifacts — navigation links, keyboard shortcuts, breadcrumbs, version badges, sidebar content, etc. that repeat across pages.

Look at the HTML structure and identify which HTML elements produce these repeated artifacts. Then provide IMPROVED prune_selectors that would remove them.

Rules:
1. Keep the same content_selector ({current_analysis.selector_spec.content_selector})
2. Add NEW CSS selectors that target the UI elements leaking into the output
3. Be specific — use class names, aria attributes, roles from the HTML
4. Do NOT remove actual documentation content

Return ONLY valid JSON, no markdown fences:
{{"prune_selectors": [...], "notes": "what was added and why"}}"""

        result_text = self.llm.chat(prompt, temperature=0.1, max_tokens=1500)
        if not result_text:
            print(f"  [llm-refine] No response, keeping current selectors", file=sys.stderr)
            return current_analysis.selector_spec

        result_text = self._clean_json(result_text)

        try:
            data = json.loads(result_text)
        except json.JSONDecodeError as e:
            print(f"  [llm-refine] Invalid JSON: {e}", file=sys.stderr)
            return current_analysis.selector_spec

        new_prune = data.get("prune_selectors", [])
        notes = data.get("notes", "")

        if not new_prune:
            print(f"  [llm-refine] No new selectors suggested", file=sys.stderr)
            return current_analysis.selector_spec

        # Merge: keep old + add new
        merged = list(current_analysis.selector_spec.prune_selectors)
        added = 0
        for sel in new_prune:
            if sel not in merged:
                merged.append(sel)
                added += 1

        print(f"  [llm-refine] Added {added} new prune selectors (total: {len(merged)})", file=sys.stderr)
        print(f"  [llm-refine] Notes: {notes}", file=sys.stderr)
        for sel in new_prune:
            if sel not in current_analysis.selector_spec.prune_selectors:
                print(f"    + {sel}", file=sys.stderr)

        return SelectorSpec(
            content_selector=current_analysis.selector_spec.content_selector,
            prune_selectors=merged,
            notes=f"{current_analysis.selector_spec.notes}; Refined: {notes}",
        )

    # ------------------------------------------------------------------
    # LLM call with retry
    # ------------------------------------------------------------------

    def _llm_analyze_with_retry(
        self,
        start_url: str,
        base_url: str,
        start_html: str,
        sample_links: Set[str],
        sample_htmls: Optional[List[str]] = None,
    ) -> LLMAnalysis:
        """Try LLM analysis up to MAX_LLM_RETRIES times with feedback on failure."""
        feedback = None

        for attempt in range(MAX_LLM_RETRIES + 1):
            if attempt > 0:
                print(f"  [llm-analyzer] Retry {attempt}/{MAX_LLM_RETRIES} with feedback...", file=sys.stderr)

            analysis = self._llm_analyze(
                start_url, base_url, start_html, sample_links,
                sample_htmls=sample_htmls,
                extra_context=feedback,
            )

            # Validate scope against sample links
            if sample_links:
                matching, non_matching, match_details = self._validate_scope(
                    analysis.scope_rules, sample_links, start_url
                )

                if matching >= 3:
                    print(f"  [llm-analyzer] Scope validation OK: {matching}/{len(sample_links)} links match", file=sys.stderr)
                    return analysis

                # Build feedback for retry
                doc_links = [l for l in sample_links if self._looks_like_doc_url(l, start_url)]
                feedback = self._build_retry_feedback(
                    matching, len(sample_links), match_details,
                    analysis.scope_rules, doc_links[:10]
                )
            else:
                return analysis

        # All retries failed — use smart path-based fallback
        print(f"  [llm-analyzer] All retries failed, using path-based fallback", file=sys.stderr)
        return self._smart_fallback(start_url, base_url, start_html, sample_links, analysis)

    def _llm_analyze(
        self,
        start_url: str,
        base_url: str,
        start_html: str,
        sample_links: Set[str],
        sample_htmls: Optional[List[str]] = None,
        extra_context: Optional[str] = None,
    ) -> LLMAnalysis:
        link_summary = self._build_link_summary(sample_links)
        clean_html = self._sanitize_html(start_html)

        sample_section = ""
        if sample_htmls:
            sample_clean = self._sanitize_html(sample_htmls[0])[:8000]
            sample_section = f"\n\n### Sample Content Page HTML (truncated):\n```html\n{sample_clean}\n```"

        feedback_section = ""
        if extra_context:
            feedback_section = f"\n\n### FEEDBACK FROM PREVIOUS ATTEMPT:\n{extra_context}\n"

        # Show some example full URLs so LLM understands the format
        example_urls = sorted(sample_links)[:10]
        example_section = "\n".join(f"  {u}" for u in example_urls)

        prompt = f"""You are analyzing a documentation website to extract it programmatically.

**Start URL:** {start_url}
**Base URL:** {base_url}

**Main Page HTML (truncated):**
```html
{clean_html}
```
{sample_section}
{feedback_section}

**Links discovered on site (grouped by path prefix):**
{link_summary}

**Example full URLs from the site:**
{example_section}

Analyze this and return a JSON object with TWO sections:

1. **scope_rules** — which URLs to include/exclude:
   - include_patterns: Python regex patterns matching documentation page URL PATHS
   - exclude_patterns: Python regex patterns matching non-doc URL PATHS

2. **selector_spec** — how to extract content from each page:
   - content_selector: CSS selector for the main content container
   - prune_selectors: CSS selectors for elements to REMOVE inside the content
   - notes: brief notes about site structure

**CRITICAL RULES for patterns:**
1. Patterns are matched against the URL PATH (e.g., "/docs/quickstart"), NOT the full URL
2. Use simple path patterns like "/docs/" — this matches any URL whose path contains "/docs/"
3. The start URL path is "{urlparse(start_url).path}" — your include patterns MUST match this path
4. Be generous with includes — include API refs, guides, tutorials, getting-started
5. Exclude: blog, news, pricing, login, social, downloads, other languages

**CRITICAL RULES for selectors:**
1. content_selector must target the MAIN content area, not the whole page
2. Look at the HTML carefully — find the element that wraps the actual documentation text
3. prune_selectors remove UI fragments INSIDE the content area (nav, feedback, TOC, etc.)

**EXAMPLES of good patterns:**
- For https://example.com/docs/intro → include: ["/docs/"]
- For https://fastapi.tiangolo.com/tutorial/ → include: ["/tutorial/", "/advanced/", "/reference/"]
- Exclude: ["/blog/", "/pricing/", "/login/", "/changelog/"]

Return ONLY valid JSON, no markdown fences:
{{"scope_rules": {{"include_patterns": [...], "exclude_patterns": [...]}}, "selector_spec": {{"content_selector": "...", "prune_selectors": [...], "notes": "..."}}}}"""

        print(f"  [llm-analyzer] Calling model: {self.model}", file=sys.stderr)
        result_text = self.llm.chat(prompt, temperature=0.1, max_tokens=2000)

        if not result_text:
            print(f"  [llm-analyzer] LLM returned no response after retries", file=sys.stderr)
            return self._smart_fallback(start_url, base_url, start_html, sample_links, None)

        # --- Verbose logging ---
        print(f"  [llm-analyzer] Raw LLM response ({len(result_text)} chars):", file=sys.stderr)
        # Print first 500 chars of response for debugging
        preview = result_text[:500]
        for line in preview.split("\n"):
            print(f"    | {line}", file=sys.stderr)
        if len(result_text) > 500:
            print(f"    | ... ({len(result_text) - 500} more chars)", file=sys.stderr)

        result_text = self._clean_json(result_text)

        try:
            data = json.loads(result_text)
        except json.JSONDecodeError as e:
            print(f"  [llm-analyzer] Invalid JSON from LLM: {e}", file=sys.stderr)
            print(f"  [llm-analyzer] Raw text: {result_text[:200]}", file=sys.stderr)
            return self._fallback(start_url, base_url, start_html)

        scope_data = data.get("scope_rules", {})
        includes = self._validate_patterns(scope_data.get("include_patterns", []))
        excludes = self._validate_patterns(scope_data.get("exclude_patterns", []))

        sel_data = data.get("selector_spec", {})

        # --- Log decisions ---
        print(f"  [llm-analyzer] Include patterns ({len(includes)}):", file=sys.stderr)
        for p in includes:
            print(f"    + {p}", file=sys.stderr)
        print(f"  [llm-analyzer] Exclude patterns ({len(excludes)}):", file=sys.stderr)
        for p in excludes[:10]:
            print(f"    - {p}", file=sys.stderr)
        if len(excludes) > 10:
            print(f"    ... and {len(excludes) - 10} more", file=sys.stderr)
        print(f"  [llm-analyzer] Content selector: {sel_data.get('content_selector', 'main')}", file=sys.stderr)
        print(f"  [llm-analyzer] Prune selectors: {sel_data.get('prune_selectors', [])}", file=sys.stderr)
        print(f"  [llm-analyzer] Notes: {sel_data.get('notes', 'none')}", file=sys.stderr)

        scope_rules = ScopeRules(
            include_patterns=includes,
            exclude_patterns=excludes,
            base_url=base_url,
            description=sel_data.get("notes", "LLM-generated"),
        )

        selector_spec = SelectorSpec(
            content_selector=sel_data.get("content_selector", "main"),
            prune_selectors=sel_data.get("prune_selectors", []),
            notes=sel_data.get("notes", ""),
        )

        return LLMAnalysis(scope_rules=scope_rules, selector_spec=selector_spec)

    # ------------------------------------------------------------------
    # Fallback heuristics
    # ------------------------------------------------------------------

    def _fallback(self, start_url: str, base_url: str, start_html: str) -> LLMAnalysis:
        """Heuristic fallback using start_url path as include pattern."""
        content_selector = self._detect_content_selector(start_html)

        # Derive include pattern from start URL path
        parsed = urlparse(start_url)
        path_parts = parsed.path.strip("/").split("/")
        include_patterns = []
        if path_parts and path_parts[0]:
            include_patterns = [f"/{path_parts[0]}/"]
            print(f"  [llm-analyzer] Heuristic fallback: include pattern = '/{path_parts[0]}/' (from start URL)", file=sys.stderr)
        else:
            print(f"  [llm-analyzer] Heuristic fallback: no path prefix, including all", file=sys.stderr)

        scope_rules = ScopeRules(
            include_patterns=include_patterns,
            exclude_patterns=[r"/blog/", r"/news/", r"/pricing/", r"/login/", r"/changelog/"],
            base_url=base_url,
            description=f"Heuristic fallback from path: {parsed.path}",
        )
        selector_spec = SelectorSpec(
            content_selector=content_selector,
            prune_selectors=FALLBACK_PRUNE_SELECTORS,
            notes="Heuristic fallback — LLM unavailable or failed",
        )
        return LLMAnalysis(scope_rules=scope_rules, selector_spec=selector_spec)

    def _detect_content_selector(self, html: str) -> str:
        if not html:
            return "main"
        soup = BeautifulSoup(html, "html.parser")
        for sel in FALLBACK_CONTENT_SELECTORS:
            if soup.select_one(sel):
                return sel
        return "body"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _build_link_summary(self, links: Set[str]) -> str:
        from urllib.parse import urlparse
        groups: Dict[str, List[str]] = defaultdict(list)
        for link in sorted(links):
            parsed = urlparse(link)
            segments = parsed.path.strip("/").split("/")
            key = f"/{segments[0]}/" if segments and segments[0] else "/"
            groups[key].append(parsed.path)

        parts = []
        for key in sorted(groups.keys()):
            paths = groups[key]
            parts.append(f"\n{key} ({len(paths)} URLs)")
            for p in paths[:5]:
                parts.append(f"  {p}")
            if len(paths) > 5:
                parts.append(f"  ... and {len(paths) - 5} more")
        return "\n".join(parts)

    @staticmethod
    def _sanitize_html(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript", "iframe", "object", "embed"]):
            tag.decompose()
        text = str(soup)[:15000]
        text = text.replace('"""', "'''")
        return text

    @staticmethod
    def _clean_json(text: str) -> str:
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    @staticmethod
    def _validate_patterns(patterns: List[str]) -> List[str]:
        valid = []
        for p in patterns:
            try:
                re.compile(p)
                valid.append(p)
            except re.error as e:
                print(f"    [llm-analyzer] Dropping invalid regex '{p}': {e}", file=sys.stderr)
        return valid

    # ------------------------------------------------------------------
    # Scope validation & retry helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_scope(
        scope_rules: ScopeRules, sample_links: Set[str], start_url: str
    ) -> tuple:
        """Validate scope rules against sample links.

        Key check: the start URL itself MUST match. Then count how many
        sample links match overall. We consider validation successful if
        the start URL matches AND at least 3 total links match.

        Returns (matching_count, non_matching_count, details_list).
        """
        matching = 0
        non_matching = 0
        details = []

        # Critical: does the start URL itself match?
        start_matches = scope_rules.url_matches(start_url)
        if not start_matches:
            start_path = urlparse(start_url).path
            print(f"  [llm-analyzer] ⚠ Start URL path '{start_path}' does NOT match scope rules!", file=sys.stderr)

        for link in sample_links:
            matches = scope_rules.url_matches(link)
            if matches:
                matching += 1
            else:
                non_matching += 1
                if len(details) < 20:
                    path = urlparse(link).path
                    reason = "no include match"
                    for pat in scope_rules.exclude_patterns:
                        try:
                            if re.search(pat, path, re.IGNORECASE):
                                reason = f"excluded by '{pat}'"
                                break
                        except re.error:
                            continue
                    details.append({"url": link, "path": path, "reason": reason})

        print(f"  [llm-analyzer] Scope validation: {matching} match, {non_matching} rejected (of {len(sample_links)} total)", file=sys.stderr)
        if not start_matches:
            # If start URL doesn't match, that's a critical failure regardless of count
            print(f"  [llm-analyzer] CRITICAL: Start URL excluded by own scope rules", file=sys.stderr)
            return 0, non_matching, details

        if details[:5]:
            print(f"  [llm-analyzer] Sample rejections:", file=sys.stderr)
            for d in details[:5]:
                print(f"    ✗ {d['path']} — {d['reason']}", file=sys.stderr)

        return matching, non_matching, details

    @staticmethod
    def _looks_like_doc_url(url: str, start_url: str) -> bool:
        """Heuristic: does this URL look like a documentation page?"""
        path = urlparse(url).path.lower()
        start_path = urlparse(start_url).path.lower().split("/")[1] if len(urlparse(start_url).path.split("/")) > 1 else ""

        # Same path prefix as start URL
        if start_path and f"/{start_path}/" in path:
            return True

        doc_signals = ["/docs/", "/doc/", "/guide/", "/tutorial/", "/api/",
                       "/reference/", "/learn/", "/manual/", "/handbook/",
                       "/getting-started", "/quickstart", "/overview"]
        return any(sig in path for sig in doc_signals)

    @staticmethod
    def _build_retry_feedback(
        matching: int, total: int, details: list,
        scope_rules: ScopeRules, doc_links: List[str]
    ) -> str:
        """Build feedback message for LLM retry."""
        lines = [
            f"Your previous scope rules only matched {matching}/{total} discovered links.",
            f"This means almost no documentation pages would be crawled.",
            "",
            "REJECTED URLs that should have been INCLUDED:",
        ]
        for d in details[:10]:
            lines.append(f"  ✗ {d['path']} — rejected because: {d['reason']}")

        if doc_links:
            lines.append("")
            lines.append("These URLs look like documentation pages and MUST be matched by your include patterns:")
            for link in doc_links[:10]:
                lines.append(f"  → {urlparse(link).path}")

        lines.extend([
            "",
            "COMMON MISTAKES TO AVOID:",
            "1. Do NOT use ^ anchored patterns like '^/docs/' — use '/docs/' instead (substring match)",
            "2. Your include patterns are matched against URL PATHS like '/docs/quickstart'",
            "3. Make sure your include patterns actually match the start URL path",
            f"4. The start URL path that MUST match: '{urlparse(doc_links[0]).path if doc_links else 'unknown'}'",
        ])

        return "\n".join(lines)

    def _smart_fallback(
        self, start_url: str, base_url: str, start_html: str,
        sample_links: Set[str], last_analysis: LLMAnalysis
    ) -> LLMAnalysis:
        """Smart fallback when all LLM retries fail.

        Uses the start URL path to derive include patterns instead of including everything.
        Keeps the LLM's selector_spec if available.
        """
        parsed = urlparse(start_url)
        path_parts = parsed.path.strip("/").split("/")

        # Use first path segment as include pattern
        if path_parts and path_parts[0]:
            include_pattern = f"/{path_parts[0]}/"
            print(f"  [llm-analyzer] Smart fallback: include pattern = '{include_pattern}'", file=sys.stderr)
        else:
            include_pattern = None

        scope_rules = ScopeRules(
            include_patterns=[include_pattern] if include_pattern else [],
            exclude_patterns=[r"/blog/", r"/news/", r"/pricing/", r"/login/", r"/changelog/"],
            base_url=base_url,
            description=f"Smart fallback from start URL path: {parsed.path}",
        )

        # Validate this fallback scope
        if sample_links:
            matching = sum(1 for link in sample_links if scope_rules.url_matches(link))
            print(f"  [llm-analyzer] Smart fallback matches {matching}/{len(sample_links)} links", file=sys.stderr)

        # Keep LLM's selector spec if it had one, otherwise use heuristic
        selector_spec = last_analysis.selector_spec if last_analysis else SelectorSpec(
            content_selector=self._detect_content_selector(start_html),
            prune_selectors=FALLBACK_PRUNE_SELECTORS,
        )

        return LLMAnalysis(scope_rules=scope_rules, selector_spec=selector_spec)
