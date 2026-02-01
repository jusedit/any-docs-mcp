import os
import re
import time
from urllib.parse import urljoin, urlparse
from collections import defaultdict
from typing import Optional, List, Dict
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from urllib.parse import urljoin, urlparse
import re
from models import DocumentationConfig, ScrapedPage, SiteAnalysis
from sitemap_parser import SitemapParser
from storage import StorageManager


class ScraperEngine:
    def __init__(self, config: DocumentationConfig, storage: StorageManager, request_delay: float = 0.2):
        self.config = config
        self.storage = storage
        self.request_delay = request_delay
        self.analysis = config.site_analysis
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"  Error fetching {url}: {e}")
            return None
    
    def extract_navigation_links(self, start_url: str) -> List[Dict[str, str]]:
        print(f"Extracting navigation links from {start_url}...")
        
        # First, try to use sitemap (best for complete coverage)
        parsed_url = urlparse(start_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        sitemap_parser = SitemapParser(base_url)
        if sitemap_parser.has_sitemap():
            print("✓ Sitemap found! Using sitemap for complete URL extraction...")
            sitemap_links = sitemap_parser.parse_sitemap()
            
            # Filter links to match URL pattern
            filtered_links = []
            for link in sitemap_links:
                if re.match(self.analysis.url_pattern, link['url']):
                    filtered_links.append(link)
            
            if filtered_links:
                print(f"✓ Extracted {len(filtered_links)} URLs from sitemap")
                return filtered_links
            else:
                print("! Sitemap found but no matching URLs, falling back to navigation parsing")
        else:
            print("! No sitemap found, using navigation parsing")
        
        # Fallback: Parse navigation from HTML
        soup = self.fetch_page(start_url)
        
        if not soup:
            print("Failed to fetch base page")
            return []
        
        links = []
        seen_urls = set()
        
        for selector in self.analysis.navigation_selectors:
            nav_element = soup.select_one(selector)
            if nav_element:
                print(f"  Found navigation using selector: {selector}")
                
                # Find all <a> tags with href
                for a in nav_element.find_all('a', href=True):
                    href = a.get('href', '')
                    
                    if href.startswith('#'):
                        continue
                    
                    full_url = urljoin(start_url, href)
                    full_url = full_url.split('#')[0]
                    
                    if not re.match(self.analysis.url_pattern, full_url):
                        continue
                    
                    if full_url not in seen_urls:
                        seen_urls.add(full_url)
                        title = a.get_text(strip=True)
                        if title:
                            links.append({'url': full_url, 'title': title})
                
                # Also find links in data attributes (common in collapsible menus)
                for elem in nav_element.find_all(attrs={'data-href': True}):
                    href = elem.get('data-href', '')
                    if href and not href.startswith('#'):
                        full_url = urljoin(start_url, href)
                        full_url = full_url.split('#')[0]
                        
                        if re.match(self.analysis.url_pattern, full_url) and full_url not in seen_urls:
                            seen_urls.add(full_url)
                            title = elem.get_text(strip=True)
                            if title:
                                links.append({'url': full_url, 'title': title})
                
                # Find links in onclick attributes (JavaScript navigation)
                for elem in nav_element.find_all(attrs={'onclick': True}):
                    onclick = elem.get('onclick', '')
                    # Extract URLs from onclick="location.href='...'" or window.location='...'
                    url_match = re.search(r"['\"]([^'\"]+)['\"]", onclick)
                    if url_match:
                        href = url_match.group(1)
                        if not href.startswith('#'):
                            full_url = urljoin(start_url, href)
                            full_url = full_url.split('#')[0]
                            
                            if re.match(self.analysis.url_pattern, full_url) and full_url not in seen_urls:
                                seen_urls.add(full_url)
                                title = elem.get_text(strip=True)
                                if title:
                                    links.append({'url': full_url, 'title': title})
                
                break
        
        print(f"Found {len(links)} documentation links")
        return links
    
    def extract_content(self, soup: BeautifulSoup) -> str:
        content_div = None
        
        for selector in self.analysis.content_selectors:
            content_div = soup.select_one(selector)
            if content_div:
                break
        
        if not content_div:
            return ""
        
        content_copy = content_div.__copy__()
        
        for selector in self.analysis.exclude_selectors:
            for element in content_copy.select(selector):
                element.decompose()
        
        markdown_content = md(
            str(content_copy),
            heading_style="ATX",
            code_language_callback=lambda el: el.get("class", [""])[0].replace("language-", "") if el.get("class") else ""
        )
        
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
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
    
    def scrape_all(self, version: str) -> Dict[str, int]:
        links = self.extract_navigation_links(self.config.start_url)
        
        if not links:
            print("No links found. Trying to scrape just the start URL...")
            links = [{'url': self.config.start_url, 'title': 'Documentation'}]
        
        url_to_group = {link['url']: self.get_url_group(link['url']) for link in links}
        
        group_counts = defaultdict(int)
        for group in url_to_group.values():
            group_counts[group] += 1
        
        print(f"\nWill create {len(group_counts)} files:")
        sorted_groups = sorted(group_counts.items(), key=lambda x: -x[1])[:10]
        for group, count in sorted_groups:
            print(f"  {group}.md: {count} pages")
        if len(group_counts) > 10:
            print(f"  ... and {len(group_counts) - 10} more")
        print()
        
        initialized_files = set()
        page_counts = defaultdict(int)
        
        for i, link in enumerate(links, 1):
            url = link['url']
            title = link['title']
            group = url_to_group[url]
            
            print(f"[{i}/{len(links)}] {url}")
            
            soup = self.fetch_page(url)
            if not soup:
                continue
            
            content = self.extract_content(soup)
            if not content:
                print("  -> No content extracted")
                continue
            
            actual_title = self.extract_title(soup, title)
            
            output_path = self.storage.get_output_file_path(self.config.name, version, group)
            
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
            
            page_counts[group] += 1
            print(f"  -> {group}.md")
            
            time.sleep(self.request_delay)
        
        print(f"\n{'='*60}")
        print(f"Scraping complete! Created {len(initialized_files)} files")
        print(f"{'='*60}")
        
        return dict(page_counts)
