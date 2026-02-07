"""Sitemap parser for extracting all URLs from documentation sites."""
import gzip
import io
import re
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from datetime import datetime


class SitemapParser:
    """Parse XML sitemaps to extract documentation URLs."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self._sitemap_urls = None  # Cache for discovered sitemap URLs
    
    def discover_sitemap_urls(self) -> List[str]:
        """Discover sitemap URLs from standard locations and robots.txt."""
        if self._sitemap_urls is not None:
            return self._sitemap_urls
        
        urls = []
        
        # 1. Try standard sitemap.xml
        standard = f"{self.base_url}/sitemap.xml"
        if self._check_url_exists(standard):
            urls.append(standard)
        
        # 2. Try sitemap-index.xml (common alternative)
        index_alt = f"{self.base_url}/sitemap-index.xml"
        if not urls and self._check_url_exists(index_alt):
            urls.append(index_alt)
        
        # 3. Check robots.txt for Sitemap: directive
        robots_urls = self._parse_robots_txt()
        for url in robots_urls:
            if url not in urls:
                urls.append(url)
        
        self._sitemap_urls = urls
        return urls
    
    def _check_url_exists(self, url: str) -> bool:
        """Check if a URL returns 200 OK."""
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            return response.status_code == 200
        except:
            return False
    
    def _parse_robots_txt(self) -> List[str]:
        """Parse robots.txt for Sitemap: directives."""
        urls = []
        try:
            robots_url = f"{self.base_url}/robots.txt"
            response = requests.get(robots_url, timeout=10)
            if response.status_code == 200:
                for line in response.text.split('\n'):
                    # Match Sitemap: <url> directive
                    match = re.match(r'^Sitemap:\s*(.+)$', line, re.IGNORECASE)
                    if match:
                        url = match.group(1).strip()
                        if url:
                            urls.append(url)
        except Exception as e:
            print(f"Failed to parse robots.txt: {e}")
        return urls
    
    def get_sitemap_url(self) -> str:
        """Get the sitemap URL, trying common locations."""
        urls = self.discover_sitemap_urls()
        return urls[0] if urls else f"{self.base_url}/sitemap.xml"
    
    def parse_sitemap(self, refresh_after: Optional[datetime] = None) -> List[Dict[str, str]]:
        """
        Parse sitemap and return list of URLs with titles.
        
        Args:
            refresh_after: Only return URLs with lastmod > this date
            
        Returns:
            List of dicts with 'url', 'title', and optionally 'lastmod' keys
        """
        sitemap_urls = self.discover_sitemap_urls()
        
        if not sitemap_urls:
            print("No sitemap discovered")
            return []
        
        all_links = []
        for sitemap_url in sitemap_urls:
            links = self._parse_sitemap_file(sitemap_url, refresh_after)
            all_links.extend(links)
        
        print(f"Extracted {len(all_links)} URLs from sitemap(s)")
        return all_links
    
    def _parse_sitemap_file(self, sitemap_url: str, refresh_after: Optional[datetime] = None) -> List[Dict[str, str]]:
        """Parse a single sitemap file (handles both .xml and .xml.gz)."""
        try:
            print(f"Fetching sitemap from {sitemap_url}...")
            response = requests.get(sitemap_url, timeout=30)
            response.raise_for_status()
            
            # Handle gzipped sitemaps
            content = response.content
            if sitemap_url.endswith('.gz') or response.headers.get('content-type') == 'application/gzip':
                content = gzip.decompress(content)
            
            # Parse XML
            root = ET.fromstring(content)
            
            # Handle XML namespace
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            links = []
            
            # Check if this is a sitemap index (contains other sitemaps)
            sitemap_elements = root.findall('.//ns:sitemap', namespace)
            if sitemap_elements:
                print(f"Found sitemap index with {len(sitemap_elements)} sub-sitemaps...")
                for sitemap_elem in sitemap_elements:
                    loc_elem = sitemap_elem.find('ns:loc', namespace)
                    if loc_elem is not None and loc_elem.text:
                        sub_links = self._parse_sitemap_file(loc_elem.text, refresh_after)
                        links.extend(sub_links)
            else:
                # This is a regular sitemap
                links = self._parse_single_sitemap_from_root(root, namespace, refresh_after)
            
            return links
            
        except Exception as e:
            print(f"Failed to parse sitemap {sitemap_url}: {e}")
            return []
    
    def _parse_single_sitemap(self, sitemap_url: str, namespace: dict, refresh_after: Optional[datetime] = None) -> List[Dict[str, str]]:
        """Parse a single sitemap file."""
        return self._parse_sitemap_file(sitemap_url, refresh_after)
    
    def _parse_single_sitemap_from_root(self, root: ET.Element, namespace: dict, refresh_after: Optional[datetime] = None) -> List[Dict[str, str]]:
        """Extract URLs from a sitemap root element."""
        links = []
        
        # Find all <url> elements
        url_elements = root.findall('.//ns:url', namespace)
        
        for url_elem in url_elements:
            loc_elem = url_elem.find('ns:loc', namespace)
            if loc_elem is not None and loc_elem.text:
                url = loc_elem.text.strip()
                
                # Check lastmod date if filter is set
                if refresh_after is not None:
                    lastmod_elem = url_elem.find('ns:lastmod', namespace)
                    if lastmod_elem is not None and lastmod_elem.text:
                        try:
                            # Parse ISO date format
                            lastmod_str = lastmod_elem.text[:10]  # Get just YYYY-MM-DD
                            lastmod_date = datetime.strptime(lastmod_str, '%Y-%m-%d')
                            if lastmod_date < refresh_after:
                                continue  # Skip URLs not modified since refresh_after
                        except ValueError:
                            pass  # If date parsing fails, include the URL
                
                # Extract title from URL path (last segment)
                path = url.replace(self.base_url, '').strip('/')
                title = path.replace('/', ' > ').replace('-', ' ').title()
                
                links.append({
                    'url': url,
                    'title': title if title else 'Documentation Page'
                })
        
        return links
    
    def has_sitemap(self) -> bool:
        """Check if a sitemap exists at the standard location."""
        return len(self.discover_sitemap_urls()) > 0
