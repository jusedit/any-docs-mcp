import hashlib
import os
import re
import sys
import time
import json
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse
from collections import defaultdict
from typing import Optional, List, Dict, Callable, Tuple
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from models import DocumentationConfig, ScrapedPage, SiteAnalysis, ScrapeProgress, SourceType
from sitemap_parser import SitemapParser
from storage import StorageManager
from content_cleaner import ContentCleaner
from url_discovery import URLDiscovery


class ScraperEngine:
    def __init__(self, config: DocumentationConfig, storage: StorageManager, 
                 max_workers: int = 10,
                 progress_callback: Optional[Callable[[ScrapeProgress], None]] = None,
                 json_progress: bool = False):
        self.config = config
        self.storage = storage
        self.max_workers = max_workers
        self.content_cleaner = ContentCleaner()
        self.url_discovery = URLDiscovery()
        self.discovery_result = None  # Stores URL discovery result with mode, version, etc.
        self.analysis = config.site_analysis
        self.progress_callback = progress_callback
        self.json_progress = json_progress
        self.content_hashes: List[str] = []
        self._progress_lock = threading.Lock()
        self._file_locks: Dict[str, threading.Lock] = {}
        self._file_locks_lock = threading.Lock()
        self._scraped_count = 0
        self._total_count = 0
    
    def _report_progress(self, phase: str, current: int = 0, total: int = 0, 
                         current_url: Optional[str] = None, message: Optional[str] = None):
        progress = ScrapeProgress(
            phase=phase,
            current=current,
            total=total,
            current_url=current_url,
            message=message
        )
        if self.progress_callback:
            self.progress_callback(progress)
        if self.json_progress:
            print(f"PROGRESS:{json.dumps(progress.model_dump())}", flush=True)
    
    def _compute_content_hash(self, content: str) -> str:
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def get_combined_hash(self) -> str:
        combined = ''.join(sorted(self.content_hashes))
        return hashlib.md5(combined.encode('utf-8')).hexdigest()
    
    def fetch_page(self, url: str, max_retries: int = 3) -> Optional[Tuple[BeautifulSoup, SourceType]]:
        """Fetch page with exponential backoff on errors. Skips 404/410 immediately.
        
        Returns:
            Tuple of (BeautifulSoup, SourceType) or None on failure.
        """
        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                # Check Content-Type header for markdown
                content_type = response.headers.get('Content-Type', '').lower()
                if 'text/markdown' in content_type or 'text/x-markdown' in content_type:
                    # Raw markdown content - wrap in HTML structure
                    markdown_content = response.text
                    html_wrapper = f'<html><body><div class="raw-markdown">{markdown_content}</div></body></html>'
                    return (BeautifulSoup(html_wrapper, 'html.parser'), SourceType.RAW_MARKDOWN)
                
                # Special handling for raw GitHub content (plaintext markdown)
                if 'raw.githubusercontent.com' in url:
                    # Wrap plaintext in a simple HTML structure for consistent processing
                    markdown_content = response.text
                    html_wrapper = f'<html><body><div class="raw-markdown">{markdown_content}</div></body></html>'
                    return (BeautifulSoup(html_wrapper, 'html.parser'), SourceType.RAW_MARKDOWN)
                
                return (BeautifulSoup(response.text, 'html.parser'), SourceType.HTML)
            except requests.HTTPError as e:
                # Don't retry 404/410 - page doesn't exist
                if e.response is not None and e.response.status_code in (404, 410, 403, 401):
                    return None
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    print(f"  Retry {attempt + 1}/{max_retries} for {url} after {wait_time:.1f}s: {e}", file=sys.stderr)
                    time.sleep(wait_time)
                else:
                    print(f"  Failed after {max_retries} attempts: {url}: {e}", file=sys.stderr)
                    return None
            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    print(f"  Retry {attempt + 1}/{max_retries} for {url} after {wait_time:.1f}s: {e}", file=sys.stderr)
                    time.sleep(wait_time)
                else:
                    print(f"  Failed after {max_retries} attempts: {url}: {e}", file=sys.stderr)
                    return None
        return None
    
    def _get_file_lock(self, group: str) -> threading.Lock:
        """Get or create a lock for a specific file group."""
        with self._file_locks_lock:
            if group not in self._file_locks:
                self._file_locks[group] = threading.Lock()
            return self._file_locks[group]
    
    def extract_navigation_links(self, start_url: str, max_pages: int = 500) -> List[Dict[str, str]]:
        """
        Extract documentation URLs using multi-mode discovery.
        Tries: sitemap -> navigation -> crawl (in order of preference)
        """
        print(f"Discovering documentation URLs from {start_url}...")
        
        # Use the new multi-mode URL discovery system
        self.discovery_result = self.url_discovery.discover_urls(start_url, max_pages)
        
        urls = self.discovery_result['urls']
        mode = self.discovery_result['mode']
        version = self.discovery_result.get('version')
        
        print(f"[OK] Discovered {len(urls)} URLs using {mode.upper()} mode")
        if version:
            print(f"  Detected documentation version: {version}")
        
        return urls
    
    def extract_content(self, soup: BeautifulSoup, source_type: SourceType = SourceType.HTML) -> str:
        # If raw markdown source, extract directly without markdownify
        if source_type == SourceType.RAW_MARKDOWN:
            raw_markdown_div = soup.find('div', class_='raw-markdown')
            if raw_markdown_div:
                # This is raw markdown content, return as-is
                raw_content = raw_markdown_div.get_text()
                return raw_content.strip()
        
        content_div = None
        
        for selector in self.analysis.content_selectors:
            try:
                content_div = soup.select_one(selector)
                if content_div:
                    break
            except Exception:
                # Skip invalid selectors
                continue
        
        if not content_div:
            # Fallback: try common content selectors
            fallback_selectors = ['main', 'article', '.content', '#content', '.main-content', '.documentation']
            for selector in fallback_selectors:
                try:
                    content_div = soup.select_one(selector)
                    if content_div:
                        break
                except Exception:
                    continue
        
        if not content_div:
            return ""
        
        content_copy = content_div.__copy__()
        
        for selector in self.analysis.exclude_selectors:
            try:
                for element in content_copy.select(selector):
                    element.decompose()
            except Exception:
                # Skip invalid selectors
                continue
        
        markdown_content = md(
            str(content_copy),
            heading_style="ATX",
            code_language_callback=lambda el: el.get("class", [""])[0].replace("language-", "") if el.get("class") else ""
        )
        
        # Apply content cleaning to remove UI artifacts and fix issues
        markdown_content = self.content_cleaner.clean(markdown_content)
        
        return markdown_content.strip()
    
    def extract_title(self, soup: BeautifulSoup, fallback: str) -> str:
        if self.analysis.title_selector:
            title_elem = soup.select_one(self.analysis.title_selector)
            if title_elem:
                return title_elem.get_text(strip=True)
        
        h1 = soup.select_one('h1')
        if h1:
            return h1.get_text(strip=True)
        
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        
        return fallback
    
    def get_url_group(self, url: str) -> str:
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        
        parts = [p for p in path.split('/') if p and not p.endswith('.html')]
        
        strategy = self.analysis.grouping_strategy
        
        if strategy == 'single_file':
            return self.config.name
        elif strategy.startswith('path_depth_'):
            try:
                depth = int(strategy.split('_')[-1])
                if len(parts) >= depth:
                    return '-'.join(parts[:depth])
                elif parts:
                    return '-'.join(parts)
                else:
                    return 'index'
            except ValueError:
                return '-'.join(parts[:2]) if len(parts) >= 2 else (parts[0] if parts else 'index')
        else:
            return '-'.join(parts[:2]) if len(parts) >= 2 else (parts[0] if parts else 'index')
    
    def _scrape_single_page(self, link: Dict[str, str], url_to_group: Dict[str, str], 
                              version: str, initialized_files: set, 
                              page_counts: Dict[str, int]) -> Optional[Tuple[str, str]]:
        """Scrape a single page. Returns (group, content_hash) or None on failure."""
        url = link['url']
        title = link['title']
        group = url_to_group[url]
        
        result = self.fetch_page(url)
        if not result:
            return None
        
        soup, source_type = result
        
        content = self.extract_content(soup, source_type)
        
        # Graceful fallback: if raw markdown content is too short, try HTML extraction
        if source_type == SourceType.RAW_MARKDOWN and len(content.strip()) < 50:
            print(f"  [WARNING] Raw markdown content too short ({len(content)} chars), trying HTML fallback for {url}", file=sys.stderr)
            # Re-fetch as HTML by modifying URL to non-raw version if possible
            # For GitHub raw URLs, convert to blob URL
            if 'raw.githubusercontent.com' in url:
                # Convert back to blob URL: https://github.com/owner/repo/blob/branch/path
                parts = url.replace('https://raw.githubusercontent.com/', '').split('/')
                if len(parts) >= 3:
                    owner, repo, branch = parts[0], parts[1], parts[2]
                    path = '/'.join(parts[3:])
                    blob_url = f"https://github.com/{owner}/{repo}/blob/{branch}/{path}"
                    html_result = self.fetch_page(blob_url)
                    if html_result:
                        soup, _ = html_result
                        content = self.extract_content(soup, SourceType.HTML)
            
            if not content or len(content.strip()) < 50:
                print(f"  [ERROR] Fallback failed or content still too short for {url}", file=sys.stderr)
                return None
        
        if not content:
            return None
        
        content_hash = self._compute_content_hash(content)
        actual_title = self.extract_title(soup, title)
        
        output_path = self.storage.get_output_file_path(self.config.name, version, group)
        
        # Use file-specific lock for thread-safe file writing
        file_lock = self._get_file_lock(group)
        with file_lock:
            if group not in initialized_files:
                header = f"# {group.replace('-', ' ').title()}\n\n"
                header += f"*Documentation: {self.config.display_name}*\n\n"
                header += "---\n\n"
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(header)
                
                initialized_files.add(group)
            
            page_md = f"## {actual_title}\n\n"
            page_md += f"**Source:** {url}\n\n"
            page_md += content
            page_md += "\n\n---\n\n"
            
            with open(output_path, 'a', encoding='utf-8') as f:
                f.write(page_md)
            
            page_counts[group] = page_counts.get(group, 0) + 1
        
        # Update progress
        with self._progress_lock:
            self._scraped_count += 1
            self._report_progress('scraping', self._scraped_count, self._total_count, current_url=url)
            print(f"[{self._scraped_count}/{self._total_count}] {url} -> {group}.md", file=sys.stderr)
        
        return (group, content_hash)
    
    def scrape_all(self, version: str, max_pages: int = 500) -> Dict[str, int]:
        self._report_progress('discovering', message='Discovering documentation URLs...')
        links = self.extract_navigation_links(self.config.start_url, max_pages)
        
        if not links:
            print("No links found. Trying to scrape just the start URL...", file=sys.stderr)
            links = [{'url': self.config.start_url, 'title': 'Documentation'}]
        
        # Limit pages to prevent runaway scrapes
        if len(links) > max_pages:
            print(f"[WARNING] Limiting from {len(links)} to {max_pages} pages", file=sys.stderr)
            links = links[:max_pages]
        
        url_to_group = {link['url']: self.get_url_group(link['url']) for link in links}
        
        group_counts = defaultdict(int)
        for group in url_to_group.values():
            group_counts[group] += 1
        
        print(f"\nWill create {len(group_counts)} files:", file=sys.stderr)
        sorted_groups = sorted(group_counts.items(), key=lambda x: -x[1])[:10]
        for group, count in sorted_groups:
            print(f"  {group}.md: {count} pages", file=sys.stderr)
        if len(group_counts) > 10:
            print(f"  ... and {len(group_counts) - 10} more", file=sys.stderr)
        print(file=sys.stderr)
        
        self._total_count = len(links)
        self._scraped_count = 0
        self._report_progress('scraping', 0, len(links), message=f'Found {len(links)} pages to scrape (using {self.max_workers} workers)')
        
        # Thread-safe collections
        initialized_files: set = set()
        page_counts: Dict[str, int] = {}
        self.content_hashes = []
        
        print(f"\n[STARTED] Starting concurrent scraping with {self.max_workers} workers...\n", file=sys.stderr)
        
        # Use ThreadPoolExecutor for concurrent scraping
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all scraping tasks
            future_to_link = {
                executor.submit(
                    self._scrape_single_page, 
                    link, url_to_group, version, initialized_files, page_counts
                ): link for link in links
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_link):
                result = future.result()
                if result:
                    group, content_hash = result
                    with self._progress_lock:
                        self.content_hashes.append(content_hash)
        
        total_pages = sum(page_counts.values())
        total_files = len(set(page_counts.keys()))
        
        self._report_progress('completed', len(links), len(links), 
                              message=f'Scraped {total_pages} pages into {total_files} files')
        
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"Scraping complete! Created {total_files} files", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)
        
        return dict(page_counts)
