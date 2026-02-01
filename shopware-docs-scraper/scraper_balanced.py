#!/usr/bin/env python3
"""
Shopware Developer Docs Scraper - Balanced Version

Scrapes the Shopware Developer Documentation and saves each page as Markdown.
Uses smart grouping to create ~50 balanced files for optimal LLM context.
"""

import os
import re
import time
from urllib.parse import urljoin, urlparse
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


BASE_URL = "https://developer.shopware.com/docs/"
OUTPUT_DIR = "output_balanced"
REQUEST_DELAY = 0.1
TARGET_FILES = 50
MAX_PAGES_PER_FILE = 40  # Split threshold - results in ~50 files


def get_path_parts(url: str) -> list[str]:
    """Extract path parts from URL after /docs/ (directories only, no .html files)"""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    
    if path.startswith("docs/"):
        path = path[5:]
    
    parts = []
    for p in path.split("/"):
        if p.endswith(".html"):
            continue
        if p:
            parts.append(p)
    
    return parts


def calculate_optimal_grouping(urls: list[str]) -> dict[str, str]:
    """
    Calculate optimal filename for each URL targeting ~50 files.
    Phase 1: Split large groups using deeper paths
    Phase 2: Merge very small groups with their parent
    """
    
    def count_at_depth(url_list: list[str], depth: int) -> dict[str, list[str]]:
        groups = defaultdict(list)
        for url in url_list:
            parts = get_path_parts(url)
            key = "-".join(parts[:depth]) if len(parts) >= depth else "-".join(parts) if parts else "index"
            groups[key].append(url)
        return groups
    
    # Phase 1: Start at depth 2, split large groups recursively
    final_groups = {}  # group_name -> list of URLs
    
    def split_if_needed(group_urls: list[str], current_depth: int, max_depth: int = 5):
        groups = count_at_depth(group_urls, current_depth)
        
        for group_name, group_url_list in groups.items():
            name = group_name if group_name else "index"
            
            if len(group_url_list) <= MAX_PAGES_PER_FILE:
                final_groups[name] = group_url_list
            elif current_depth >= max_depth:
                # Split by number
                chunk_size = MAX_PAGES_PER_FILE
                for i in range(0, len(group_url_list), chunk_size):
                    chunk = group_url_list[i:i+chunk_size]
                    part_num = (i // chunk_size) + 1
                    final_groups[f"{name}-part{part_num}"] = chunk
            else:
                deeper = count_at_depth(group_url_list, current_depth + 1)
                if len(deeper) > 1:
                    split_if_needed(group_url_list, current_depth + 1, max_depth)
                else:
                    # Can't split deeper - split by number
                    chunk_size = MAX_PAGES_PER_FILE
                    for i in range(0, len(group_url_list), chunk_size):
                        chunk = group_url_list[i:i+chunk_size]
                        part_num = (i // chunk_size) + 1
                        final_groups[f"{name}-part{part_num}"] = chunk
    
    split_if_needed(urls, 2)
    
    # Phase 2: Merge small groups (< 5 pages) with related groups
    # Group by depth-1 prefix and merge tiny ones
    merged_groups = {}
    tiny_groups = defaultdict(list)  # parent -> [(name, urls), ...]
    
    for name, group_urls in final_groups.items():
        if len(group_urls) < 5:
            # Get parent prefix (first part before -)
            parent = name.split("-")[0] if "-" in name else name
            tiny_groups[parent].append((name, group_urls))
        else:
            merged_groups[name] = group_urls
    
    # Merge tiny groups into parent buckets
    for parent, tiny_list in tiny_groups.items():
        all_urls = []
        for name, urls in tiny_list:
            all_urls.extend(urls)
        
        if all_urls:
            # Create merged group with parent name + "-misc" or just parent
            merged_name = parent
            if merged_name in merged_groups:
                merged_name = f"{parent}-misc"
            merged_groups[merged_name] = all_urls
    
    # Build final URL to filename mapping
    url_to_filename = {}
    for group_name, group_urls in merged_groups.items():
        for url in group_urls:
            url_to_filename[url] = group_name
    
    return url_to_filename


def get_output_filename(url: str, url_to_filename: dict[str, str]) -> str:
    """Get the pre-calculated filename for this URL."""
    return url_to_filename.get(url, "misc")


def fetch_page(url: str) -> BeautifulSoup | None:
    """Fetch a page and return BeautifulSoup object."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"  Error fetching {url}: {e}")
        return None


def extract_sidebar_links(soup: BeautifulSoup, base_url: str) -> list[dict]:
    """Extract all links from #VPSidebarNav in order."""
    links = []
    seen_urls = set()
    
    sidebar = soup.select_one("#VPSidebarNav")
    if not sidebar:
        print("Warning: #VPSidebarNav not found")
        return links
    
    for a in sidebar.find_all("a", href=True):
        href = a.get("href", "")
        
        if href.startswith("#") or (href.startswith("http") and "developer.shopware.com" not in href):
            continue
        
        full_url = urljoin(base_url, href)
        
        if "/docs/" not in full_url:
            continue
        
        full_url = full_url.split("#")[0]
        
        if full_url not in seen_urls:
            seen_urls.add(full_url)
            title = a.get_text(strip=True)
            links.append({"url": full_url, "title": title})
    
    return links


def extract_main_content(soup: BeautifulSoup) -> str:
    """Extract main content and convert to Markdown."""
    content_div = soup.select_one("#VPContent main.main .vp-doc")
    
    if not content_div:
        content_div = soup.select_one("#VPContent .vp-doc")
    if not content_div:
        content_div = soup.select_one(".vp-doc")
    if not content_div:
        content_div = soup.select_one("main.main")
    if not content_div:
        return ""
    
    for element in content_div.select("nav, .sidebar, .toc, .edit-link, .prev-next, footer, .VPDocFooter, .SwagRelatedArticles, .SwagDocFeedback, .SwagAlgoliaAttributes"):
        element.decompose()
    
    markdown_content = md(str(content_div), heading_style="ATX", code_language_callback=lambda el: el.get("class", [""])[0].replace("language-", "") if el.get("class") else "")
    markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)
    
    return markdown_content.strip()


def scrape_docs():
    """Main scraping function with balanced grouping."""
    print(f"Starting balanced scrape of {BASE_URL}")
    print(f"Max {MAX_PAGES_PER_FILE} pages per file\n")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Fetch sidebar links
    print("Fetching base page for sidebar links...")
    base_soup = fetch_page(BASE_URL)
    
    if not base_soup:
        print("Failed to fetch base page. Exiting.")
        return
    
    sidebar_links = extract_sidebar_links(base_soup, BASE_URL)
    print(f"Found {len(sidebar_links)} links in sidebar\n")
    
    # Calculate optimal grouping
    print("Calculating optimal file grouping...")
    urls = [link["url"] for link in sidebar_links]
    url_to_filename = calculate_optimal_grouping(urls)
    
    # Preview grouping
    file_preview = defaultdict(int)
    for link in sidebar_links:
        filename = get_output_filename(link["url"], url_to_filename)
        file_preview[filename] += 1
    
    print(f"Will create {len(file_preview)} files:")
    sorted_preview = sorted(file_preview.items(), key=lambda x: -x[1])
    for fname, count in sorted_preview[:15]:
        print(f"  {fname}.md: {count} pages")
    if len(sorted_preview) > 15:
        print(f"  ... and {len(sorted_preview) - 15} more files")
    print()
    
    # Scrape and write
    initialized_files = set()
    page_counts = defaultdict(int)
    
    for i, link in enumerate(sidebar_links, 1):
        url = link["url"]
        title = link["title"]
        filename = get_output_filename(url, url_to_filename)
        output_path = os.path.join(OUTPUT_DIR, f"{filename}.md")
        
        print(f"[{i}/{len(sidebar_links)}] Fetching: {url}")
        
        soup = fetch_page(url)
        
        if soup:
            content = extract_main_content(soup)
            if content:
                if filename not in initialized_files:
                    header = f"# {filename.replace('-', ' ').title()}\n\n"
                    header += f"*Scraped from Shopware Developer Documentation*\n\n"
                    header += "---\n\n"
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(header)
                    initialized_files.add(filename)
                
                page_md = f"## {title}\n\n"
                page_md += f"**Source:** {url}\n\n"
                page_md += content
                page_md += "\n\n---\n\n"
                
                with open(output_path, "a", encoding="utf-8") as f:
                    f.write(page_md)
                
                page_counts[filename] += 1
                print(f"  -> Written to {filename}.md")
            else:
                print(f"  -> No content found")
        
        time.sleep(REQUEST_DELAY)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Done! Created {len(initialized_files)} files in {OUTPUT_DIR}/")
    print(f"{'='*60}\n")
    
    # Show file sizes
    sorted_counts = sorted(page_counts.items(), key=lambda x: -x[1])
    print("Files by page count:")
    for fname, count in sorted_counts:
        print(f"  {fname}.md: {count} pages")


if __name__ == "__main__":
    scrape_docs()
