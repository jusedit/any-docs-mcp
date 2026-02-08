"""FR2: Discovery Worker — robots.txt, sitemap, quick-sample, canonicalize.

Discovers documentation URLs from a start URL using multiple strategies:
1. robots.txt → sitemap references
2. Standard sitemap paths (/sitemap.xml, /sitemap-index.xml, etc.)
3. Quick-sample: BFS crawl of ~10 pages from start URL for link extraction
4. Canonicalize + dedupe all discovered URLs into a frontier
"""
import gzip
import re
import sys
import xml.etree.ElementTree as ET
from collections import deque
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from models import EngineMode, UrlRecord

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


SKIP_EXTENSIONS = frozenset({
    ".pdf", ".zip", ".tar", ".gz", ".png", ".jpg", ".jpeg", ".gif", ".svg",
    ".css", ".js", ".woff", ".woff2", ".ttf", ".ico", ".xml", ".json",
    ".mp4", ".mp3", ".webm", ".webp", ".avif",
})

MAX_SITEMAP_URLS = 5000

STANDARD_SITEMAP_PATHS = [
    "/sitemap.xml",
    "/sitemap_index.xml",
    "/sitemap-index.xml",
    "/sitemap1.xml",
]


class DiscoveryWorker:
    def __init__(self, timeout: int = 15, engine_mode: EngineMode = EngineMode.CURL):
        self.timeout = timeout
        self.engine_mode = engine_mode
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; AnyDocsMCP/2.0)"
        })
        self._driver = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def discover(self, start_url: str, max_sample_pages: int = 10) -> Tuple[List[UrlRecord], str, Set[str]]:
        """Run full discovery pipeline.

        Returns:
            (frontier, start_page_html, all_raw_links)
            - frontier: deduplicated UrlRecords
            - start_page_html: HTML of start page (for LLM analyzer)
            - all_raw_links: every unique link found during scout crawl
        """
        parsed = urlparse(start_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        start_path = parsed.path.rstrip("/") or ""

        # 1. Sitemap URLs
        sitemap_urls = self._discover_sitemap_urls(base_url)
        print(f"  [discovery] Sitemap URLs found: {len(sitemap_urls)}", file=sys.stderr)

        # 1b. Pre-filter sitemap URLs by start_url path prefix
        if start_path and start_path != "/":
            before_filter = len(sitemap_urls)
            sitemap_urls = [
                u for u in sitemap_urls
                if urlparse(u["url"]).path.rstrip("/").startswith(start_path)
            ]
            if before_filter != len(sitemap_urls):
                print(f"  [discovery] Path pre-filter ({start_path}): {before_filter} → {len(sitemap_urls)}", file=sys.stderr)

        # 2. Quick-sample BFS
        start_html, sample_links = self._quick_sample(start_url, max_pages=max_sample_pages)
        print(f"  [discovery] Quick-sample found {len(sample_links)} unique links", file=sys.stderr)

        # 3. Merge + canonicalize + dedupe
        frontier: Dict[str, UrlRecord] = {}

        for url_dict in sitemap_urls:
            canon = self._canonicalize(url_dict["url"], base_url)
            if canon and canon not in frontier:
                frontier[canon] = UrlRecord(
                    url=canon,
                    title=url_dict.get("title", ""),
                    source="sitemap",
                )

        for link in sample_links:
            canon = self._canonicalize(link, base_url)
            if canon and canon not in frontier:
                frontier[canon] = UrlRecord(
                    url=canon,
                    title="",
                    source="quick-sample",
                )

        records = list(frontier.values())
        print(f"  [discovery] Frontier: {len(records)} unique URLs", file=sys.stderr)
        return records, start_html, sample_links

    # ------------------------------------------------------------------
    # Sitemap discovery
    # ------------------------------------------------------------------

    def _discover_sitemap_urls(self, base_url: str) -> List[Dict[str, str]]:
        sitemap_locations = self._find_sitemap_locations(base_url)
        all_urls: List[Dict[str, str]] = []
        for loc in sitemap_locations:
            all_urls.extend(self._parse_sitemap(loc))
        return all_urls

    def _find_sitemap_locations(self, base_url: str) -> List[str]:
        locations: List[str] = []

        # robots.txt
        try:
            resp = self.session.get(f"{base_url}/robots.txt", timeout=self.timeout)
            if resp.status_code == 200:
                for line in resp.text.splitlines():
                    m = re.match(r"^Sitemap:\s*(.+)$", line, re.IGNORECASE)
                    if m:
                        locations.append(m.group(1).strip())
        except Exception:
            pass

        # Standard paths (only if robots.txt didn't yield any)
        if not locations:
            for path in STANDARD_SITEMAP_PATHS:
                url = base_url + path
                try:
                    resp = self.session.head(url, timeout=self.timeout, allow_redirects=True)
                    if resp.status_code == 200:
                        locations.append(url)
                        break
                except Exception:
                    continue

        return locations

    def _parse_sitemap(self, sitemap_url: str, depth: int = 0, _count: list = None) -> List[Dict[str, str]]:
        if _count is None:
            _count = [0]
        if depth > 3 or _count[0] >= MAX_SITEMAP_URLS:
            return []
        try:
            resp = self.session.get(sitemap_url, timeout=30)
            resp.raise_for_status()
            content = resp.content
            if sitemap_url.endswith(".gz") or "gzip" in resp.headers.get("content-type", ""):
                content = gzip.decompress(content)
            root = ET.fromstring(content)
        except Exception as e:
            print(f"  [discovery] Failed to parse sitemap {sitemap_url}: {e}", file=sys.stderr)
            return []

        ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        results: List[Dict[str, str]] = []

        # Sitemap index?
        for sm in root.findall(".//ns:sitemap", ns):
            if _count[0] >= MAX_SITEMAP_URLS:
                break
            loc = sm.find("ns:loc", ns)
            if loc is not None and loc.text:
                results.extend(self._parse_sitemap(loc.text.strip(), depth + 1, _count))

        # Regular URL entries
        for url_el in root.findall(".//ns:url", ns):
            if _count[0] >= MAX_SITEMAP_URLS:
                print(f"  [discovery] Sitemap cap reached ({MAX_SITEMAP_URLS} URLs)", file=sys.stderr)
                break
            loc = url_el.find("ns:loc", ns)
            if loc is not None and loc.text:
                raw = loc.text.strip()
                path = urlparse(raw).path.strip("/")
                title = path.replace("/", " > ").replace("-", " ").title() if path else "Index"
                results.append({"url": raw, "title": title})
                _count[0] += 1

        return results

    # ------------------------------------------------------------------
    # Quick-sample BFS
    # ------------------------------------------------------------------

    def _quick_sample(self, start_url: str, max_pages: int = 10) -> Tuple[str, Set[str]]:
        """BFS crawl up to *max_pages* pages from start_url.

        Uses Selenium when engine_mode is SELENIUM (for SPA sites).
        Returns (start_page_html, set_of_all_discovered_links).
        """
        use_selenium = (self.engine_mode == EngineMode.SELENIUM and SELENIUM_AVAILABLE)
        if use_selenium:
            print(f"  [discovery] Using Selenium for quick-sample (SPA detected)", file=sys.stderr)
            return self._quick_sample_selenium(start_url, max_pages)
        return self._quick_sample_curl(start_url, max_pages)

    def _quick_sample_curl(self, start_url: str, max_pages: int = 10) -> Tuple[str, Set[str]]:
        """BFS crawl using requests (cURL mode)."""
        parsed_start = urlparse(start_url)
        base_url = f"{parsed_start.scheme}://{parsed_start.netloc}"

        all_links: Set[str] = set()
        visited: Set[str] = set()
        queue: deque = deque([start_url])
        start_html = ""
        pages_visited = 0

        while queue and pages_visited < max_pages:
            url = queue.popleft()
            canon = self._canonicalize(url, base_url)
            if not canon or canon in visited:
                continue
            visited.add(canon)

            try:
                resp = self.session.get(url, timeout=self.timeout)
                if resp.status_code != 200:
                    continue
                if "text/html" not in resp.headers.get("content-type", ""):
                    continue
            except Exception:
                continue

            html = resp.text
            if pages_visited == 0:
                start_html = html
            pages_visited += 1

            soup = BeautifulSoup(html, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a.get("href", "").split("#")[0].strip()
                if not href or href.startswith(("javascript:", "mailto:", "tel:")):
                    continue
                full = urljoin(url, href)
                full_parsed = urlparse(full)
                if full_parsed.netloc != parsed_start.netloc:
                    continue
                clean = f"{full_parsed.scheme}://{full_parsed.netloc}{full_parsed.path}"
                all_links.add(clean)
                if clean not in visited and self._is_navigable(clean):
                    queue.append(clean)

        return start_html, all_links

    def _quick_sample_selenium(self, start_url: str, max_pages: int = 10) -> Tuple[str, Set[str]]:
        """BFS crawl using Selenium (for SPA/client-rendered sites)."""
        parsed_start = urlparse(start_url)
        base_url = f"{parsed_start.scheme}://{parsed_start.netloc}"

        all_links: Set[str] = set()
        visited: Set[str] = set()
        queue: deque = deque([start_url])
        start_html = ""
        pages_visited = 0

        driver = self._get_driver()
        if not driver:
            print(f"  [discovery] Selenium driver init failed, falling back to cURL", file=sys.stderr)
            return self._quick_sample_curl(start_url, max_pages)

        try:
            while queue and pages_visited < max_pages:
                url = queue.popleft()
                canon = self._canonicalize(url, base_url)
                if not canon or canon in visited:
                    continue
                visited.add(canon)

                try:
                    driver.get(url)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    # Wait a bit for SPA hydration
                    import time
                    time.sleep(1)
                except Exception:
                    continue

                html = driver.page_source
                if pages_visited == 0:
                    start_html = html
                pages_visited += 1

                soup = BeautifulSoup(html, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = a.get("href", "").split("#")[0].strip()
                    if not href or href.startswith(("javascript:", "mailto:", "tel:")):
                        continue
                    full = urljoin(url, href)
                    full_parsed = urlparse(full)
                    if full_parsed.netloc != parsed_start.netloc:
                        continue
                    clean = f"{full_parsed.scheme}://{full_parsed.netloc}{full_parsed.path}"
                    all_links.add(clean)
                    if clean not in visited and self._is_navigable(clean):
                        queue.append(clean)
        finally:
            self._close_driver()

        return start_html, all_links

    def _get_driver(self):
        """Create or return existing Selenium WebDriver."""
        if self._driver:
            return self._driver
        if not SELENIUM_AVAILABLE:
            return None
        try:
            opts = ChromeOptions()
            opts.add_argument("--headless=new")
            opts.add_argument("--disable-gpu")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            opts.add_argument("--window-size=1920,1080")
            service = ChromeService(ChromeDriverManager().install())
            self._driver = webdriver.Chrome(service=service, options=opts)
            self._driver.set_page_load_timeout(30)
            return self._driver
        except Exception as e:
            print(f"  [discovery] Failed to create Selenium driver: {e}", file=sys.stderr)
            return None

    def _close_driver(self):
        """Close Selenium WebDriver if open."""
        if self._driver:
            try:
                self._driver.quit()
            except Exception:
                pass
            self._driver = None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _canonicalize(self, url: str, base_url: str) -> Optional[str]:
        if not url:
            return None
        parsed = urlparse(url)
        if not parsed.scheme:
            url = urljoin(base_url, url)
            parsed = urlparse(url)
        path = parsed.path.rstrip("/") or "/"
        return f"{parsed.scheme}://{parsed.netloc}{path}"

    @staticmethod
    def _is_navigable(url: str) -> bool:
        path = urlparse(url).path.lower()
        return not any(path.endswith(ext) for ext in SKIP_EXTENSIONS)
