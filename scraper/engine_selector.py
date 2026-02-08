"""FR1: Engine Selection — cURL vs Selenium via content-diff heuristic.

Fetches the start URL with both engines, converts to markdown preview,
and compares length/headings/code blocks to decide which engine to use.
"""
import re
import sys
from typing import Optional

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

from models import EngineDecision, EngineMode

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


def _strip_boilerplate(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "iframe", "svg"]):
        tag.decompose()
    for nav in soup.select("nav, header, footer, .cookie-banner, .newsletter"):
        nav.decompose()
    return str(soup)


def _html_to_md_preview(html: str) -> str:
    clean = _strip_boilerplate(html)
    return md(clean, heading_style="ATX", code_language_callback=lambda el: "")


def _count_headings(text: str) -> int:
    return len(re.findall(r"^#{1,6}\s+", text, re.MULTILINE))


def _count_code_blocks(text: str) -> int:
    return len(re.findall(r"^```", text, re.MULTILINE)) // 2


def _count_internal_links(html: str, start_url: str) -> int:
    """Count internal links in HTML (same domain)."""
    from urllib.parse import urlparse, urljoin
    parsed = urlparse(start_url)
    domain = parsed.netloc
    soup = BeautifulSoup(html, "html.parser")
    count = 0
    for a in soup.find_all("a", href=True):
        href = a.get("href", "")
        if not href or href.startswith(("javascript:", "mailto:", "tel:", "#")):
            continue
        full = urljoin(start_url, href)
        if urlparse(full).netloc == domain:
            count += 1
    return count


def _fetch_curl(url: str, timeout: int = 30) -> Optional[str]:
    try:
        resp = requests.get(url, timeout=timeout, headers={
            "User-Agent": "Mozilla/5.0 (compatible; AnyDocsMCP/2.0)"
        })
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"  [engine-selector] cURL fetch failed: {e}", file=sys.stderr)
        return None


def _fetch_selenium(url: str, timeout: int = 30) -> Optional[str]:
    if not SELENIUM_AVAILABLE:
        return None
    driver = None
    try:
        opts = ChromeOptions()
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--window-size=1920,1080")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=opts)
        driver.set_page_load_timeout(timeout)
        driver.get(url)
        # Wait for body first, then give SPA time to hydrate
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        # Wait up to 5s for at least one anchor link to appear (SPA hydration)
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href]"))
            )
        except Exception:
            pass
        import time
        time.sleep(1)
        return driver.page_source
    except Exception as e:
        print(f"  [engine-selector] Selenium fetch failed: {e}", file=sys.stderr)
        return None
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


def select_engine(start_url: str, threshold: float = 0.3) -> EngineDecision:
    """Compare cURL vs Selenium output and decide which engine to use.

    Decision rule (v1 heuristic):
    - If Selenium produces significantly more content (headings, code blocks, length),
      choose Selenium.
    - Otherwise default to cURL (faster, lighter).
    """
    print(f"  [engine-selector] Testing cURL...", file=sys.stderr)
    curl_html = _fetch_curl(start_url)
    curl_md = _html_to_md_preview(curl_html) if curl_html else ""
    curl_headings = _count_headings(curl_md)
    curl_code = _count_code_blocks(curl_md)
    curl_links = _count_internal_links(curl_html, start_url) if curl_html else 0

    sel_md = ""
    sel_headings = 0
    sel_code = 0
    sel_links = 0

    if SELENIUM_AVAILABLE:
        print(f"  [engine-selector] Testing Selenium...", file=sys.stderr)
        sel_html = _fetch_selenium(start_url)
        sel_md = _html_to_md_preview(sel_html) if sel_html else ""
        sel_headings = _count_headings(sel_md)
        sel_code = _count_code_blocks(sel_md)
        sel_links = _count_internal_links(sel_html, start_url) if sel_html else 0
    else:
        print(f"  [engine-selector] Selenium not available, defaulting to cURL", file=sys.stderr)
        return EngineDecision(
            mode=EngineMode.CURL,
            curl_md_length=len(curl_md),
            reason="Selenium not installed"
        )

    max_len = max(len(curl_md), len(sel_md), 1)
    diff_ratio = abs(len(sel_md) - len(curl_md)) / max_len

    heading_diff = sel_headings - curl_headings
    code_diff = sel_code - curl_code

    choose_selenium = False
    reasons = []

    if diff_ratio > threshold and len(sel_md) > len(curl_md):
        choose_selenium = True
        reasons.append(f"content length diff {diff_ratio:.1%} > {threshold:.0%}")

    if heading_diff > 3:
        choose_selenium = True
        reasons.append(f"Selenium has {heading_diff} more headings")

    if code_diff > 2:
        choose_selenium = True
        reasons.append(f"Selenium has {code_diff} more code blocks")

    # SPA detection: cURL has very few links but Selenium has many
    if curl_links < 5 and sel_links > 10:
        choose_selenium = True
        reasons.append(f"SPA detected: cURL {curl_links} links vs Selenium {sel_links} links")

    mode = EngineMode.SELENIUM if choose_selenium else EngineMode.CURL
    reason = "; ".join(reasons) if reasons else "cURL content sufficient"

    decision = EngineDecision(
        mode=mode,
        curl_md_length=len(curl_md),
        selenium_md_length=len(sel_md),
        curl_headings=curl_headings,
        selenium_headings=sel_headings,
        curl_code_blocks=curl_code,
        selenium_code_blocks=sel_code,
        diff_ratio=diff_ratio,
        reason=reason,
    )
    print(f"  [engine-selector] Decision: {mode.value} ({reason})", file=sys.stderr)
    return decision
