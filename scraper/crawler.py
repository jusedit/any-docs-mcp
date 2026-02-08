"""FR4: Crawler & Transform — Frontier queue, fetch, extract, clean, HTML→MD, write 1:1.

Processes a filtered URL frontier:
1. Fetch each URL (cURL or Selenium mode)
2. Extract main content via CSS selector
3. Prune UI fragments
4. Convert HTML → Markdown
5. Write 1 file per URL path (1:1 mapping)
6. Build manifest with path↔URL, size, headings, hash
"""
import hashlib
import os
import random
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

from content_cleaner import ContentCleaner
from models import (
    EngineMode,
    Manifest,
    ManifestEntry,
    SelectorSpec,
    UrlRecord,
)

SELENIUM_AVAILABLE = False
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    SELENIUM_AVAILABLE = True
except ImportError:
    pass


class Crawler:
    def __init__(
        self,
        engine_mode: EngineMode,
        selector_spec: SelectorSpec,
        output_dir: str,
        max_workers: int = 10,
        max_retries: int = 3,
    ):
        self.engine_mode = engine_mode
        self.selector_spec = selector_spec
        self.output_dir = Path(output_dir)
        self.raw_dir = self.output_dir / "md" / "raw"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.max_workers = max_workers
        self.max_retries = max_retries
        self.cleaner = ContentCleaner()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; AnyDocsMCP/2.0)"
        })
        self._lock = threading.Lock()
        self._scraped = 0
        self._total = 0
        self._driver = None
        self._driver_lock = threading.Lock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def crawl(self, frontier: List[UrlRecord]) -> Manifest:
        """Crawl all URLs in frontier and write 1:1 markdown files.

        Returns a Manifest with all entries.
        """
        self._total = len(frontier)
        self._scraped = 0
        entries: List[ManifestEntry] = []

        print(f"  [crawler] Crawling {self._total} URLs with {self.max_workers} workers ({self.engine_mode.value} mode)", file=sys.stderr)

        if self.engine_mode == EngineMode.SELENIUM:
            # Selenium: single-threaded to share browser instance
            for record in frontier:
                entry = self._process_url(record)
                if entry:
                    entries.append(entry)
        else:
            # cURL: concurrent
            with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
                futures = {pool.submit(self._process_url, rec): rec for rec in frontier}
                for future in as_completed(futures):
                    entry = future.result()
                    if entry:
                        with self._lock:
                            entries.append(entry)

        manifest = Manifest(
            start_url=frontier[0].url if frontier else "",
            engine_mode=self.engine_mode.value,
            total_pages=len(entries),
            total_files=len(entries),
            entries=entries,
        )
        return manifest

    # ------------------------------------------------------------------
    # Per-URL processing
    # ------------------------------------------------------------------

    def _process_url(self, record: UrlRecord) -> Optional[ManifestEntry]:
        html = self._fetch(record.url)
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")
        markdown = self._extract_and_convert(soup)
        if not markdown or len(markdown.strip()) < 20:
            return None

        # Build output path from URL path
        rel_path = self._url_to_filepath(record.url)
        out_path = self.raw_dir / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # Extract title
        title = self._extract_title(soup, record.title)

        # Write file
        content = f"# {title}\n\n**Source:** {record.url}\n\n{markdown}\n"
        out_path.write_text(content, encoding="utf-8")

        # Build manifest entry
        headings = re.findall(r"^(#{1,6}\s+.+)$", markdown, re.MULTILINE)
        content_hash = hashlib.md5(content.encode("utf-8")).hexdigest()

        with self._lock:
            self._scraped += 1
            print(f"  [{self._scraped}/{self._total}] {record.url} → {rel_path}", file=sys.stderr)

        return ManifestEntry(
            url=record.url,
            md_raw_path=str(rel_path),
            size_bytes=len(content.encode("utf-8")),
            headings=[h.strip() for h in headings[:20]],
            content_hash=content_hash,
        )

    # ------------------------------------------------------------------
    # Fetch
    # ------------------------------------------------------------------

    def _fetch(self, url: str) -> Optional[str]:
        if self.engine_mode == EngineMode.SELENIUM:
            return self._fetch_selenium(url)
        return self._fetch_curl(url)

    def _fetch_curl(self, url: str) -> Optional[str]:
        for attempt in range(self.max_retries):
            try:
                resp = self.session.get(url, timeout=30)
                if resp.status_code in (404, 410, 403, 401):
                    return None
                resp.raise_for_status()
                return resp.text
            except requests.HTTPError:
                if attempt < self.max_retries - 1:
                    time.sleep((2 ** attempt) + random.uniform(0, 1))
                else:
                    return None
            except requests.RequestException:
                if attempt < self.max_retries - 1:
                    time.sleep((2 ** attempt) + random.uniform(0, 1))
                else:
                    return None
        return None

    def _fetch_selenium(self, url: str) -> Optional[str]:
        if not SELENIUM_AVAILABLE:
            print(f"  [crawler] Selenium not available, skipping {url}", file=sys.stderr)
            return None
        with self._driver_lock:
            if self._driver is None:
                opts = ChromeOptions()
                opts.add_argument("--headless=new")
                opts.add_argument("--disable-gpu")
                opts.add_argument("--no-sandbox")
                opts.add_argument("--disable-dev-shm-usage")
                service = ChromeService(ChromeDriverManager().install())
                self._driver = webdriver.Chrome(service=service, options=opts)
                self._driver.set_page_load_timeout(30)
        try:
            self._driver.get(url)
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            # Wait for SPA hydration: look for content selector or any anchor
            try:
                sel = self.selector_spec.content_selector
                WebDriverWait(self._driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, sel))
                )
            except Exception:
                try:
                    WebDriverWait(self._driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href]"))
                    )
                except Exception:
                    pass
            import time
            time.sleep(0.5)
            return self._driver.page_source
        except Exception as e:
            print(f"  [crawler] Selenium error for {url}: {e}", file=sys.stderr)
            return None

    def close(self):
        if self._driver:
            try:
                self._driver.quit()
            except Exception:
                pass
            self._driver = None

    # ------------------------------------------------------------------
    # Extract & Convert
    # ------------------------------------------------------------------

    def _extract_and_convert(self, soup: BeautifulSoup) -> str:
        # Find main content
        content_el = None
        selector = self.selector_spec.content_selector
        try:
            content_el = soup.select_one(selector)
        except Exception:
            pass

        if not content_el:
            for fallback in ["main", "article", ".content", "#content", "body"]:
                try:
                    content_el = soup.select_one(fallback)
                    if content_el:
                        break
                except Exception:
                    continue

        if not content_el:
            return ""

        # Clone to avoid mutating original
        from copy import copy
        content_copy = copy(content_el)

        # Prune unwanted elements
        for prune_sel in self.selector_spec.prune_selectors:
            try:
                for el in content_copy.select(prune_sel):
                    el.decompose()
            except Exception:
                continue

        # Also prune common UI elements that often leak through
        for generic_sel in ["script", "style", "noscript", "iframe", "aside",
                            "button[aria-label*='copy']", "button[aria-label*='Copy']",
                            ".copy-button", ".clipboard-button"]:
            try:
                for el in content_copy.select(generic_sel):
                    el.decompose()
            except Exception:
                continue

        # Generic sidebar detection: remove fixed/sticky elements with many links
        self._prune_sidebar_elements(content_copy)

        # Pre-process code blocks to preserve newlines
        self._preprocess_code_blocks(content_copy)

        # Convert to markdown
        markdown = md(
            str(content_copy),
            heading_style="ATX",
            code_language_callback=lambda el: (
                el.get("class", [""])[0].replace("language-", "")
                if el.get("class") else ""
            ),
        )

        # Clean
        markdown = self.cleaner.clean(markdown)
        return markdown.strip()

    @staticmethod
    def _prune_sidebar_elements(soup_el):
        """Generically detect and remove sidebar navigation inside content.

        Heuristics:
        1. Elements with fixed/sticky positioning + many links = sidebar nav
        2. Direct children of content with nav-like classes + many links
        """
        MIN_LINKS_FOR_SIDEBAR = 8

        for el in list(soup_el.find_all(recursive=False)):
            classes = " ".join(el.get("class", []))
            style = el.get("style", "")

            # Check for fixed/sticky positioning (via class or style)
            is_fixed = any(kw in classes for kw in ["fixed", "sticky"]) or \
                       any(kw in style for kw in ["position: fixed", "position: sticky"])

            # Check for nav-like class names
            is_nav_like = any(kw in classes.lower() for kw in [
                "sidebar", "sidenav", "side-nav", "toc", "table-of-contents",
                "navigation", "nav-menu", "menu-panel",
            ])

            if is_fixed or is_nav_like:
                link_count = len(el.find_all("a"))
                if link_count >= MIN_LINKS_FOR_SIDEBAR:
                    el.decompose()

    @staticmethod
    def _preprocess_code_blocks(soup_el):
        """Fix code blocks before markdownify conversion.

        markdownify often concatenates lines inside <pre>/<code> blocks.
        Common patterns handled:
        - Shiki: <pre><code><span class="line">...</span></code></pre>
        - Highlight.js: <pre><code><span>line1</span><br>...</code></pre>
        - Generic: <pre><div>line</div>...</pre>
        """
        from bs4 import NavigableString, Tag

        for pre in soup_el.find_all("pre"):
            # Strategy 1: Shiki-style — span.line elements represent code lines
            line_spans = pre.find_all("span", class_=lambda c: c and isinstance(c, list) and "line" in c)
            if not line_spans:
                # Also try string match for class attribute
                line_spans = [s for s in pre.find_all("span") if s.get("class") and "line" in s.get("class", [])]

            if line_spans:
                for span in line_spans:
                    span.append(NavigableString("\n"))
                    span.unwrap()
                # Unwrap remaining styling spans
                for span in list(pre.find_all("span")):
                    span.unwrap()
                continue

            # Strategy 2: <br> tags as line separators
            for br in pre.find_all("br"):
                br.replace_with(NavigableString("\n"))

            # Strategy 3: Block elements inside pre (div, p)
            for tag_name in ["div", "p", "li"]:
                for el in pre.find_all(tag_name):
                    el.insert_before(NavigableString("\n"))
                    el.unwrap()

            # Unwrap remaining inline elements (spans) inside pre
            for span in list(pre.find_all("span")):
                span.unwrap()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _url_to_filepath(url: str) -> str:
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        if not path:
            path = "index"
        # Remove file extension if present
        if path.endswith(".html") or path.endswith(".htm"):
            path = path.rsplit(".", 1)[0]
        # Sanitize
        path = re.sub(r"[^\w/\-.]", "_", path)
        return path + ".md"

    @staticmethod
    def _extract_title(soup: BeautifulSoup, fallback: str) -> str:
        h1 = soup.select_one("h1")
        if h1:
            return h1.get_text(strip=True)[:200]
        title_tag = soup.find("title")
        if title_tag:
            return title_tag.get_text(strip=True)[:200]
        return fallback or "Untitled"
