#!/usr/bin/env python3
"""
Shopware Developer Docs Scraper

Scrapes the Shopware Developer Documentation and saves each page as Markdown.
Files are organized by the first two path segments after /docs/ (e.g., guides-plugins.md).
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
OUTPUT_DIR = "output"
REQUEST_DELAY = 0.5  # Delay between requests to be polite


def get_output_filename(url: str) -> str:
    """
    Generate output filename from URL.
    Example: https://developer.shopware.com/docs/guides/plugins/overview -> guides-plugins.md
    """
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    
    # Remove 'docs/' prefix if present
    if path.startswith("docs/"):
        path = path[5:]
    
    parts = path.split("/")
    
    if len(parts) >= 2:
        return f"{parts[0]}-{parts[1]}"
    elif len(parts) == 1 and parts[0]:
        return parts[0]
    else:
        return "index"


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
    """
    Extract all links from #VPSidebarNav in order.
    Returns list of dicts with 'url' and 'title'.
    """
    links = []
    seen_urls = set()
    
    sidebar = soup.select_one("#VPSidebarNav")
    if not sidebar:
        print("Warning: #VPSidebarNav not found")
        return links
    
    for a in sidebar.find_all("a", href=True):
        href = a.get("href", "")
        
        # Skip anchors and external links
        if href.startswith("#") or href.startswith("http") and "developer.shopware.com" not in href:
            continue
        
        full_url = urljoin(base_url, href)
        
        # Only include URLs under /docs/
        if "/docs/" not in full_url:
            continue
        
        # Remove anchor from URL
        full_url = full_url.split("#")[0]
        
        if full_url not in seen_urls:
            seen_urls.add(full_url)
            title = a.get_text(strip=True)
            links.append({"url": full_url, "title": title})
    
    return links


def extract_main_content(soup: BeautifulSoup) -> str:
    """Extract main content from #VPContent .main .vp-doc and convert to Markdown."""
    # The actual content is in .vp-doc inside main.main
    content_div = soup.select_one("#VPContent main.main .vp-doc")
    
    if not content_div:
        # Fallback: try different selectors
        content_div = soup.select_one("#VPContent .vp-doc")
    
    if not content_div:
        content_div = soup.select_one(".vp-doc")
    
    if not content_div:
        content_div = soup.select_one("main.main")
    
    if not content_div:
        return ""
    
    # Remove navigation elements, sidebars, footers, etc.
    for element in content_div.select("nav, .sidebar, .toc, .edit-link, .prev-next, footer, .VPDocFooter, .SwagRelatedArticles, .SwagDocFeedback, .SwagAlgoliaAttributes"):
        element.decompose()
    
    # Convert to Markdown
    markdown_content = md(str(content_div), heading_style="ATX", code_language_callback=lambda el: el.get("class", [""])[0].replace("language-", "") if el.get("class") else "")
    
    # Clean up excessive newlines
    markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)
    
    return markdown_content.strip()


def scrape_docs():
    """Main scraping function."""
    print(f"Starting scrape of {BASE_URL}")
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Fetch the base page to get sidebar links
    print("Fetching base page for sidebar links...")
    base_soup = fetch_page(BASE_URL)
    
    if not base_soup:
        print("Failed to fetch base page. Exiting.")
        return
    
    # Get all sidebar links
    sidebar_links = extract_sidebar_links(base_soup, BASE_URL)
    print(f"Found {len(sidebar_links)} links in sidebar")
    
    # Group pages by output filename to maintain order within each file
    pages_by_file = defaultdict(list)
    
    for link in sidebar_links:
        filename = get_output_filename(link["url"])
        pages_by_file[filename].append(link)
    
    print(f"Will create {len(pages_by_file)} output files")
    
    # Track which files have been initialized with headers
    initialized_files = set()
    page_counts = defaultdict(int)
    
    for i, link in enumerate(sidebar_links, 1):
        url = link["url"]
        title = link["title"]
        filename = get_output_filename(url)
        output_path = os.path.join(OUTPUT_DIR, f"{filename}.md")
        
        print(f"[{i}/{len(sidebar_links)}] Fetching: {url}")
        
        soup = fetch_page(url)
        
        if soup:
            content = extract_main_content(soup)
            if content:
                # Initialize file with header if first time
                if filename not in initialized_files:
                    header = f"# {filename.replace('-', ' ').title()}\n\n"
                    header += f"*Scraped from Shopware Developer Documentation*\n\n"
                    header += "---\n\n"
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(header)
                    initialized_files.add(filename)
                
                # Append page content
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
    print(f"\nDone! Created {len(initialized_files)} files in {OUTPUT_DIR}/")
    for filename, count in page_counts.items():
        print(f"  {filename}.md: {count} pages")


if __name__ == "__main__":
    scrape_docs()
