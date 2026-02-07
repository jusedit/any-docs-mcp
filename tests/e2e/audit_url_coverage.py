"""
URL Coverage Audit: Deep-crawl documentation sites via Selenium,
then compare discovered URLs against scraped Source URLs.

Usage:
  # Crawl a single site and compare
  python audit_url_coverage.py --site react --url https://react.dev/ --max-pages 500

  # Crawl all README sites (uses known URLs)
  python audit_url_coverage.py --all --max-pages 200

  # Only compare (skip crawl, use cached crawl results)
  python audit_url_coverage.py --compare-only

  # Quick mode: use requests + BeautifulSoup instead of Selenium
  python audit_url_coverage.py --all --max-pages 200 --quick
"""
import argparse
import json
import os
import re
import sys
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse

# Add scraper to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))

APPDATA_DOCS = Path(os.environ.get("APPDATA", "")) / "AnyDocsMCP" / "docs"
RESULTS_DIR = Path(__file__).parent / "fixtures" / "real-world" / "url-coverage"

# All 50 README sites
README_SITES = {
    # Programming Languages
    "python3": "https://docs.python.org/3/",
    "nodejs": "https://nodejs.org/api/",
    "typescript": "https://www.typescriptlang.org/docs/",
    "java": "https://docs.oracle.com/en/java/javase/",
    "kotlin": "https://kotlinlang.org/docs/home.html",
    "rust-book": "https://doc.rust-lang.org/book/",
    "golang": "https://go.dev/doc/",
    "dotnet": "https://learn.microsoft.com/en-us/dotnet/",
    # Tools & Build Systems
    "git": "https://git-scm.com/docs",
    "linux-man": "https://man7.org/linux/man-pages/",
    "swagger": "https://swagger.io/docs/",
    "grpc": "https://grpc.io/docs/",
    "webpack": "https://webpack.js.org/concepts/",
    "eslint": "https://eslint.org/docs/latest/",
    "vite": "https://vite.dev/guide/",
    "tailwind": "https://tailwindcss.com/docs",
    # Web Frameworks (Frontend)
    "react": "https://react.dev/",
    "nextjs": "https://nextjs.org/docs",
    "vuejs": "https://vuejs.org/guide/",
    "nuxt": "https://nuxt.com/docs",
    "angular": "https://angular.dev/",
    "svelte": "https://svelte.dev/docs",
    "sveltekit": "https://svelte.dev/docs/kit",
    "hyperapp": "https://github.com/jorgebucaran/hyperapp",
    # Web Frameworks (Backend)
    "django": "https://docs.djangoproject.com/en/stable/",
    "flask": "https://flask.palletsprojects.com/en/stable/",
    "fastapi": "https://fastapi.tiangolo.com/",
    "rails": "https://guides.rubyonrails.org/",
    "laravel": "https://laravel.com/docs",
    "spring-boot": "https://docs.spring.io/spring-boot/reference/index.html",
    # Databases
    "postgresql": "https://www.postgresql.org/docs/current/",
    "mysql": "https://dev.mysql.com/doc/",
    "sqlite": "https://www.sqlite.org/docs.html",
    "redis": "https://redis.io/docs/latest/",
    "mongodb": "https://www.mongodb.com/docs/",
    "elasticsearch": "https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html",
    # Message Queues
    "kafka": "https://kafka.apache.org/documentation/",
    "rabbitmq": "https://www.rabbitmq.com/docs",
    # DevOps & Infrastructure
    "docker": "https://docs.docker.com/",
    "kubernetes": "https://kubernetes.io/docs/",
    "helm": "https://helm.sh/docs/",
    "terraform": "https://developer.hashicorp.com/terraform/docs",
    "ansible": "https://docs.ansible.com/ansible/latest/",
    "nginx": "https://nginx.org/en/docs/",
    # Cloud & APIs
    "github": "https://docs.github.com/en",
    "aws": "https://docs.aws.amazon.com/",
    "gcloud": "https://docs.cloud.google.com/docs",
    "azure": "https://learn.microsoft.com/en-us/azure/",
    "openai": "https://platform.openai.com/docs/overview",
    "stripe": "https://docs.stripe.com/",
    "twilio": "https://www.twilio.com/docs",
}


def extract_scraped_urls(site_name: str) -> Set[str]:
    """Extract all Source URLs from scraped .md files in AppData."""
    urls = set()
    site_dir = APPDATA_DOCS / site_name
    if not site_dir.exists():
        return urls

    # Find latest version
    versions = sorted(
        [d for d in site_dir.iterdir() if d.is_dir() and d.name.startswith("v")],
        key=lambda d: int(d.name[1:]) if d.name[1:].isdigit() else 0,
        reverse=True,
    )
    if not versions:
        return urls

    latest = versions[0]
    for md_file in latest.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8", errors="replace")
            for line in content.split("\n"):
                if "**Source:**" in line:
                    url = line.replace("**Source:**", "").strip()
                    if url.startswith("http"):
                        urls.add(normalize_url(url))
        except Exception:
            pass
    return urls


def normalize_url(url: str) -> str:
    """Normalize URL for comparison (strip fragment, trailing slash consistency)."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    if not path:
        path = ""
    return f"{parsed.scheme}://{parsed.netloc}{path}"


def is_doc_url(url: str, base_url: str) -> bool:
    """Check if URL belongs to the same documentation site."""
    parsed = urlparse(url)
    base_parsed = urlparse(base_url)

    if parsed.netloc != base_parsed.netloc:
        return False

    # Skip non-doc resources
    skip_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.css', '.js',
                       '.woff', '.woff2', '.ttf', '.eot', '.zip', '.tar', '.gz', '.pdf'}
    path_lower = parsed.path.lower()
    if any(path_lower.endswith(ext) for ext in skip_extensions):
        return False

    # Skip common non-doc paths
    skip_paths = ['/search', '/login', '/signup', '/auth', '/api/v', '/_next/',
                  '/static/', '/assets/', '/images/', '/fonts/', '/cdn-cgi/']
    if any(sp in path_lower for sp in skip_paths):
        return False

    return True


def deep_crawl_quick(start_url: str, max_pages: int = 200, timeout: int = 10) -> Set[str]:
    """BFS crawl using requests + BeautifulSoup (fast, no JS rendering)."""
    import requests
    from bs4 import BeautifulSoup

    visited = set()
    queue = deque([start_url])
    found_urls = set()
    base_parsed = urlparse(start_url)
    base_url = f"{base_parsed.scheme}://{base_parsed.netloc}"

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })

    pages_crawled = 0
    print(f"  Quick crawl: {start_url} (max {max_pages} pages)")

    while queue and pages_crawled < max_pages:
        url = queue.popleft()
        norm = normalize_url(url)
        if norm in visited:
            continue
        visited.add(norm)

        try:
            resp = session.get(url, timeout=timeout, allow_redirects=True)
            if resp.status_code != 200:
                continue
            if 'text/html' not in resp.headers.get('content-type', ''):
                continue
        except Exception:
            continue

        pages_crawled += 1
        found_urls.add(norm)

        if pages_crawled % 50 == 0:
            print(f"    ... {pages_crawled} pages crawled, {len(found_urls)} URLs found")

        soup = BeautifulSoup(resp.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href'].split('#')[0].strip()
            if not href or href.startswith(('javascript:', 'mailto:', 'tel:')):
                continue
            full = urljoin(url, href)
            full_norm = normalize_url(full)
            if full_norm not in visited and is_doc_url(full, base_url):
                queue.append(full)

    print(f"  Quick crawl done: {pages_crawled} pages visited, {len(found_urls)} unique URLs")
    return found_urls


def deep_crawl_selenium(start_url: str, max_pages: int = 200) -> Set[str]:
    """BFS crawl using Selenium WebDriver (handles JS-rendered sites)."""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
        print("  ERROR: selenium not installed. Use --quick mode or install selenium.")
        return set()

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(15)

    visited = set()
    queue = deque([start_url])
    found_urls = set()
    base_parsed = urlparse(start_url)
    base_url = f"{base_parsed.scheme}://{base_parsed.netloc}"

    pages_crawled = 0
    print(f"  Selenium crawl: {start_url} (max {max_pages} pages)")

    try:
        while queue and pages_crawled < max_pages:
            url = queue.popleft()
            norm = normalize_url(url)
            if norm in visited:
                continue
            visited.add(norm)

            try:
                driver.get(url)
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(1)
            except Exception:
                continue

            pages_crawled += 1
            found_urls.add(norm)

            if pages_crawled % 20 == 0:
                print(f"    ... {pages_crawled} pages crawled, {len(found_urls)} URLs found")

            try:
                links = driver.find_elements(By.TAG_NAME, "a")
                for link in links:
                    try:
                        href = link.get_attribute('href')
                        if not href:
                            continue
                        href = href.split('#')[0].strip()
                        if not href or href.startswith(('javascript:', 'mailto:')):
                            continue
                        full_norm = normalize_url(href)
                        if full_norm not in visited and is_doc_url(href, base_url):
                            queue.append(href)
                    except Exception:
                        continue
            except Exception:
                continue

        print(f"  Selenium crawl done: {pages_crawled} pages visited, {len(found_urls)} unique URLs")
    finally:
        driver.quit()

    return found_urls


def run_audit(site_name: str, start_url: str, max_pages: int, use_selenium: bool,
              cached: Optional[Set[str]] = None) -> Dict:
    """Run coverage audit for a single site."""
    # Step 1: Deep crawl (or use cache)
    if cached is not None:
        crawled_urls = cached
    elif use_selenium:
        crawled_urls = deep_crawl_selenium(start_url, max_pages)
    else:
        crawled_urls = deep_crawl_quick(start_url, max_pages)

    # Step 2: Extract scraped URLs
    scraped_urls = extract_scraped_urls(site_name)

    # Step 3: Compare
    crawled_normalized = {normalize_url(u) for u in crawled_urls}
    scraped_normalized = {normalize_url(u) for u in scraped_urls}

    covered = crawled_normalized & scraped_normalized
    missing = crawled_normalized - scraped_normalized
    extra = scraped_normalized - crawled_normalized  # scraped but not in crawl

    coverage = len(covered) / max(len(crawled_normalized), 1) * 100

    return {
        "site": site_name,
        "start_url": start_url,
        "crawled_count": len(crawled_normalized),
        "scraped_count": len(scraped_normalized),
        "covered_count": len(covered),
        "missing_count": len(missing),
        "extra_count": len(extra),
        "coverage_pct": round(coverage, 1),
        "missing_urls": sorted(missing)[:50],  # Cap at 50 for readability
        "extra_urls": sorted(extra)[:20],
        "crawled_urls": sorted(crawled_normalized),
    }


def save_results(results: List[Dict], output_dir: Path):
    """Save audit results to JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Per-site results
    for r in results:
        site_file = output_dir / f"{r['site']}.json"
        with open(site_file, "w", encoding="utf-8") as f:
            json.dump(r, f, indent=2, ensure_ascii=False)

    # Summary
    summary = {
        "audit_timestamp": datetime.now().isoformat(),
        "sites_audited": len(results),
        "results": []
    }
    for r in results:
        summary["results"].append({
            "site": r["site"],
            "crawled": r["crawled_count"],
            "scraped": r["scraped_count"],
            "covered": r["covered_count"],
            "missing": r["missing_count"],
            "coverage_pct": r["coverage_pct"],
        })

    summary_file = output_dir / f"summary_{timestamp}.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary_file


def print_report(results: List[Dict]):
    """Print coverage report to console."""
    print("\n" + "=" * 90)
    print("URL COVERAGE AUDIT REPORT")
    print("=" * 90)
    print(f"\n{'Site':<20} {'Crawled':>8} {'Scraped':>8} {'Covered':>8} {'Missing':>8} {'Coverage':>9}")
    print("─" * 90)

    total_crawled = 0
    total_scraped = 0
    total_covered = 0
    total_missing = 0
    problem_sites = []

    for r in sorted(results, key=lambda x: x["coverage_pct"]):
        status = "✅" if r["coverage_pct"] >= 80 else ("⚠️" if r["coverage_pct"] >= 50 else "❌")
        print(f"{status} {r['site']:<18} {r['crawled_count']:>8} {r['scraped_count']:>8} "
              f"{r['covered_count']:>8} {r['missing_count']:>8} {r['coverage_pct']:>8.1f}%")
        total_crawled += r["crawled_count"]
        total_scraped += r["scraped_count"]
        total_covered += r["covered_count"]
        total_missing += r["missing_count"]
        if r["coverage_pct"] < 80:
            problem_sites.append(r)

    print("─" * 90)
    overall = total_covered / max(total_crawled, 1) * 100
    print(f"   {'TOTAL':<18} {total_crawled:>8} {total_scraped:>8} "
          f"{total_covered:>8} {total_missing:>8} {overall:>8.1f}%")

    if problem_sites:
        print(f"\n⚠️  {len(problem_sites)} sites with coverage < 80%:")
        for r in problem_sites:
            print(f"\n  {r['site']} ({r['coverage_pct']:.1f}% coverage)")
            print(f"    Missing {r['missing_count']} URLs. Top missing:")
            for url in r["missing_urls"][:5]:
                print(f"      - {url}")

    print(f"\n{'=' * 90}")
    not_scraped = [name for name in README_SITES if not extract_scraped_urls(name)]
    if not_scraped:
        print(f"\n⚠️  {len(not_scraped)} README sites NOT scraped at all:")
        for name in not_scraped:
            print(f"    - {name} ({README_SITES[name]})")

    print()


def main():
    parser = argparse.ArgumentParser(description="URL Coverage Audit")
    parser.add_argument("--site", help="Single site name to audit")
    parser.add_argument("--url", help="Start URL (required with --site if not in README list)")
    parser.add_argument("--all", action="store_true", help="Audit all README sites that have been scraped")
    parser.add_argument("--max-pages", type=int, default=200, help="Max pages to crawl per site (default: 200)")
    parser.add_argument("--quick", action="store_true", help="Use requests instead of Selenium (faster, no JS)")
    parser.add_argument("--selenium", action="store_true", help="Force Selenium (default for JS-heavy sites)")
    parser.add_argument("--compare-only", action="store_true", help="Skip crawl, use cached results")
    parser.add_argument("--output", default=str(RESULTS_DIR), help="Output directory for results")
    args = parser.parse_args()

    output_dir = Path(args.output)
    use_selenium = args.selenium and not args.quick

    results = []

    if args.site:
        url = args.url or README_SITES.get(args.site)
        if not url:
            print(f"ERROR: No URL for site '{args.site}'. Use --url to specify.")
            sys.exit(1)

        if args.compare_only:
            cached_file = output_dir / f"{args.site}.json"
            if cached_file.exists():
                with open(cached_file) as f:
                    cached_data = json.load(f)
                cached = set(cached_data.get("crawled_urls", []))
            else:
                print(f"ERROR: No cached results for {args.site}")
                sys.exit(1)
            r = run_audit(args.site, url, args.max_pages, use_selenium, cached=cached)
        else:
            r = run_audit(args.site, url, args.max_pages, use_selenium)
        results.append(r)

    elif args.all:
        # Find which README sites have been scraped
        for site_name, url in README_SITES.items():
            scraped = extract_scraped_urls(site_name)
            if not scraped:
                print(f"  SKIP {site_name}: not scraped yet")
                continue

            print(f"\n--- {site_name} ---")
            if args.compare_only:
                cached_file = output_dir / f"{site_name}.json"
                if cached_file.exists():
                    with open(cached_file) as f:
                        cached_data = json.load(f)
                    cached = set(cached_data.get("crawled_urls", []))
                    r = run_audit(site_name, url, args.max_pages, use_selenium, cached=cached)
                else:
                    print(f"  No cached results, skipping")
                    continue
            else:
                r = run_audit(site_name, url, args.max_pages, use_selenium)
            results.append(r)
    else:
        parser.print_help()
        sys.exit(1)

    if results:
        summary_file = save_results(results, output_dir)
        print_report(results)
        print(f"Results saved to: {output_dir}")


if __name__ == "__main__":
    main()
