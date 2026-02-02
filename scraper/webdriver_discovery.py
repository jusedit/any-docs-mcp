"""
WebDriver-based URL discovery for JavaScript-heavy or bot-protected sites.
Uses Selenium/Playwright as fallback when standard requests fail.
"""
import re
import json
from typing import List, Dict, Optional, Set
from urllib.parse import urlparse, urljoin
from collections import deque

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class WebDriverDiscovery:
    """URL discovery using Selenium for JS-heavy sites."""
    
    def __init__(self):
        self.driver = None
    
    def _get_driver(self) -> Optional[object]:
        """Initialize and return Chrome WebDriver."""
        if not SELENIUM_AVAILABLE:
            return None
        
        if self.driver is None:
            try:
                options = Options()
                options.add_argument('--headless=new')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
                options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
                
                # SSL and security settings
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--ignore-ssl-errors')
                options.add_argument('--allow-insecure-localhost')
                options.add_argument('--allow-running-insecure-content')
                
                # Disable automation flags
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option('excludeSwitches', ['enable-automation'])
                options.add_experimental_option('useAutomationExtension', False)
                
                # Disable logging
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
                
                # Remove webdriver property from navigator
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
            except Exception as e:
                print(f"  WebDriver init failed: {e}")
                return None
        
        return self.driver
    
    def discover_urls(self, start_url: str, max_pages: int = 30) -> Optional[Dict]:
        """
        Discover URLs using WebDriver.
        Returns None if Selenium not available or fails.
        """
        if not SELENIUM_AVAILABLE:
            return None
        
        driver = self._get_driver()
        if not driver:
            return None
        
        try:
            print(f"  WebDriver: Loading {start_url}...")
            driver.get(start_url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Give extra time for JS to render
            import time
            time.sleep(2)
            
            parsed_start = urlparse(start_url)
            base_url = f"{parsed_start.scheme}://{parsed_start.netloc}"
            scope = self._determine_scope(start_url)
            
            urls = []
            seen = set()
            
            # Find all links on the page
            links = driver.find_elements(By.TAG_NAME, "a")
            print(f"  WebDriver: Found {len(links)} links")
            
            for link in links:
                try:
                    href = link.get_attribute('href')
                    if not href:
                        continue
                    
                    full_url = self._normalize_url(href, start_url, base_url)
                    if full_url and full_url not in seen:
                        if self._url_in_scope(full_url, base_url, scope):
                            if self._is_doc_page(full_url):
                                seen.add(full_url)
                                title = link.text.strip()[:100] or urlparse(full_url).path.split('/')[-1]
                                urls.append({'url': full_url, 'title': title})
                except:
                    continue
            
            # Limit to max_pages
            urls = urls[:max_pages]
            
            print(f"  WebDriver: {len(urls)} valid URLs found")
            
            return {
                'mode': 'webdriver',
                'urls': urls,
                'version': None,
                'scope': scope,
                'stats': {'raw': len(links), 'filtered': len(urls)}
            }
            
        except Exception as e:
            print(f"  WebDriver error: {e}")
            return None
    
    def close(self):
        """Close WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
    
    def _determine_scope(self, url: str) -> str:
        """Determine the URL scope (path prefix) for filtering."""
        parsed = urlparse(url)
        path = parsed.path.rstrip('/')
        
        if path.endswith(('.html', '.htm', '.php')):
            path = path.rsplit('.', 1)[0]
        
        for suffix in ['/home', '/index', '/docs', '/doc']:
            if path.endswith(suffix):
                path = path[:-len(suffix)]
                break
        
        if not path or path == '/':
            return '/'
        
        return path + '/'
    
    def _normalize_url(self, href: str, current_url: str, base_url: str) -> Optional[str]:
        """Normalize a URL to absolute form."""
        if not href or href.startswith('#') or href.startswith('javascript:'):
            return None
        
        if href.startswith('//'):
            return 'https:' + href
        
        if href.startswith('/'):
            return base_url + href
        
        if href.startswith('http'):
            return href
        
        return urljoin(current_url, href)
    
    def _url_in_scope(self, url: str, base_url: str, scope: str) -> bool:
        """Check if URL is within the defined scope."""
        if not url.startswith(base_url):
            return False
        
        if scope == '/':
            return True
        
        parsed = urlparse(url)
        return scope in parsed.path or parsed.path.startswith(scope.rstrip('/'))
    
    def _is_doc_page(self, url: str) -> bool:
        """Check if URL looks like a documentation page."""
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        skip_extensions = ['.pdf', '.zip', '.tar', '.gz', '.png', '.jpg', '.jpeg', 
                          '.gif', '.svg', '.css', '.js', '.xml', '.json', '.txt',
                          '.mp4', '.mp3', '.webm', '.woff', '.woff2', '.ttf', '.eot']
        if any(path.endswith(ext) for ext in skip_extensions):
            return False
        
        skip_paths = ['/search', '/login', '/logout', '/admin', '/api/', '/_', 
                     '/static/', '/assets/', '/images/', '/img/', '/fonts/',
                     '/download', '/downloads/', '/feed', '/rss', '/atom']
        if any(skip in path for skip in skip_paths):
            return False
        
        skip_params = ['utm_', 'fbclid', 'gclid', 'ref=', 'source=']
        if any(param in parsed.query.lower() for param in skip_params):
            return False
        
        return True
