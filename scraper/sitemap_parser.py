"""Sitemap parser for extracting all URLs from documentation sites."""
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict
from urllib.parse import urljoin


class SitemapParser:
    """Parse XML sitemaps to extract documentation URLs."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def get_sitemap_url(self) -> str:
        """Get the sitemap URL, trying common locations."""
        return f"{self.base_url}/sitemap.xml"
    
    def parse_sitemap(self) -> List[Dict[str, str]]:
        """
        Parse sitemap and return list of URLs with titles.
        
        Returns:
            List of dicts with 'url' and 'title' keys
        """
        sitemap_url = self.get_sitemap_url()
        
        try:
            print(f"Fetching sitemap from {sitemap_url}...")
            response = requests.get(sitemap_url, timeout=30)
            response.raise_for_status()
            
            # Parse XML
            root = ET.fromstring(response.content)
            
            # Handle XML namespace
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            links = []
            
            # Check if this is a sitemap index (contains other sitemaps)
            sitemap_elements = root.findall('.//ns:sitemap', namespace)
            if sitemap_elements:
                print("Found sitemap index, parsing sub-sitemaps...")
                for sitemap_elem in sitemap_elements:
                    loc_elem = sitemap_elem.find('ns:loc', namespace)
                    if loc_elem is not None and loc_elem.text:
                        sub_links = self._parse_single_sitemap(loc_elem.text, namespace)
                        links.extend(sub_links)
            else:
                # This is a regular sitemap
                links = self._parse_single_sitemap_from_root(root, namespace)
            
            print(f"Extracted {len(links)} URLs from sitemap")
            return links
            
        except Exception as e:
            print(f"Failed to parse sitemap: {e}")
            return []
    
    def _parse_single_sitemap(self, sitemap_url: str, namespace: dict) -> List[Dict[str, str]]:
        """Parse a single sitemap file."""
        try:
            response = requests.get(sitemap_url, timeout=30)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            return self._parse_single_sitemap_from_root(root, namespace)
        except Exception as e:
            print(f"Failed to parse sitemap {sitemap_url}: {e}")
            return []
    
    def _parse_single_sitemap_from_root(self, root: ET.Element, namespace: dict) -> List[Dict[str, str]]:
        """Extract URLs from a sitemap root element."""
        links = []
        
        # Find all <url> elements
        url_elements = root.findall('.//ns:url', namespace)
        
        for url_elem in url_elements:
            loc_elem = url_elem.find('ns:loc', namespace)
            if loc_elem is not None and loc_elem.text:
                url = loc_elem.text.strip()
                
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
        try:
            sitemap_url = self.get_sitemap_url()
            response = requests.head(sitemap_url, timeout=10)
            return response.status_code == 200
        except:
            return False
