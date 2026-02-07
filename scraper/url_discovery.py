"""
Multi-mode URL discovery for documentation scraping.

Supports three modes:
1. SITEMAP - Parse sitemap.xml for URLs
2. NAVIGATION - Extract URLs from navigation menus
3. CRAWL - Recursively follow links within a scope

The LLM determines the best mode based on site analysis.
"""
import re
import json
from typing import List, Dict, Optional, Set, Tuple
from urllib.parse import urlparse, urljoin
from collections import deque
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os

from sitemap_parser import SitemapParser
from github_discovery import GitHubDiscovery


class URLDiscovery:
    """Multi-mode URL discovery for documentation sites."""
    
    MODES = ['github', 'sitemap', 'navigation', 'crawl']
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        ) if self.api_key else None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; AnyDocsMCP/1.0)'
        })
        self.github_discovery = GitHubDiscovery()
    
    def discover_urls(self, start_url: str, max_pages: int = 500, locale_filter: Optional[str] = None) -> Dict:
        """
        Discover documentation URLs using the best available method.
        
        Args:
            start_url: The starting URL for discovery
            max_pages: Maximum number of pages to discover
            locale_filter: Optional language code to filter URLs (e.g., 'en', 'de').
                          Auto-detected from start_url if not provided.
        
        Returns:
            {
                'mode': 'sitemap' | 'navigation' | 'crawl',
                'urls': [{'url': str, 'title': str}],
                'version': str | None,
                'scope': List[str],
                'locale': str | None,
                'stats': {...}
            }
        """
        parsed = urlparse(start_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        # Detect version from URL
        version = self._detect_version(start_url)
        
        # Auto-detect locale from start_url if not provided
        if locale_filter is None:
            locale_filter = self._detect_locale(start_url)
        
        # Determine scopes (path prefixes for filtering)
        scopes = self._determine_scope(start_url)
        
        print(f"  URL Discovery for: {start_url}")
        print(f"  Detected version: {version or 'none'}")
        print(f"  Locale filter: {locale_filter or 'none'}")
        scope_str = ', '.join(scopes[:3]) + ('...' if len(scopes) > 3 else '')
        print(f"  Scopes: {scope_str}")
        
        # Try modes in order of preference
        result = None
        
        # 0. Check if it's a GitHub repository first
        if self.github_discovery.is_github_repo(start_url):
            print(f"  Detected GitHub repository")
            github_files = self.github_discovery.discover_markdown_files(start_url, max_pages)
            # Apply locale filter to GitHub results
            github_files = self._apply_locale_filter(github_files, locale_filter)
            if github_files:
                result = {
                    'mode': 'github',
                    'urls': github_files,
                    'version': version,
                    'scopes': scopes,
                    'locale': locale_filter,
                    'stats': {'raw': len(github_files), 'filtered': len(github_files)}
                }
                print(f"  Mode: GITHUB ({len(result['urls'])} markdown files)")
                return result
            else:
                print(f"  GitHub discovery found no files, falling back to other modes")
        
        # 1. Try sitemap first
        sitemap_urls = self._try_sitemap(base_url, scopes, max_pages, locale_filter)
        if sitemap_urls and len(sitemap_urls) >= 10:
            result = {
                'mode': 'sitemap',
                'urls': sitemap_urls[:max_pages],
                'version': version,
                'scopes': scopes,
                'locale': locale_filter,
                'stats': {'raw': len(sitemap_urls), 'filtered': min(len(sitemap_urls), max_pages)}
            }
            print(f"  Mode: SITEMAP ({len(result['urls'])} URLs)")
            return result
        
        # 2. Try navigation extraction
        nav_urls = self._try_navigation(start_url, scopes, locale_filter)
        if nav_urls and len(nav_urls) >= 5:
            result = {
                'mode': 'navigation',
                'urls': nav_urls[:max_pages],
                'version': version,
                'scopes': scopes,
                'locale': locale_filter,
                'stats': {'raw': len(nav_urls), 'filtered': min(len(nav_urls), max_pages)}
            }
            print(f"  Mode: NAVIGATION ({len(result['urls'])} URLs)")
            return result
        
        # 3. Fall back to crawling
        crawl_urls = self._crawl_links(start_url, scopes, max_pages, locale_filter)
        result = {
            'mode': 'crawl',
            'urls': crawl_urls[:max_pages],
            'version': version,
            'scopes': scopes,
            'locale': locale_filter,
            'stats': {'raw': len(crawl_urls), 'filtered': min(len(crawl_urls), max_pages)}
        }
        print(f"  Mode: CRAWL ({len(result['urls'])} URLs)")
        return result
    
    def _detect_locale(self, url: str) -> Optional[str]:
        """Detect language/locale from URL path.
        
        Examples:
            /en/stable/ -> 'en'
            /de/5.0/ -> 'de'
            /docs/latest/ -> None (no locale)
            /el/ (Greek Django) -> 'el'
        """
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        
        if not path:
            return None
        
        # First path segment is often the locale
        # Pattern: /{locale}/... where locale is 2-3 letters
        first_segment = path.split('/')[0]
        
        # Check if first segment looks like a locale code
        # Valid: 'en', 'de', 'fr', 'ja', 'el', 'zh-hans', etc.
        # Not valid: 'docs', 'stable', 'v1', '2024'
        if re.match(r'^[a-z]{2}(-[a-z]+)?$', first_segment):
            # Exclude common non-locale path segments
            non_locales = {'docs', 'api', 'blog', 'about', 'help', 'search', 'v1', 'v2'}
            if first_segment not in non_locales:
                return first_segment
        
        return None
    
    def _apply_locale_filter(self, urls: List[Dict], locale_filter: str) -> List[Dict]:
        """Filter URLs to only include those matching the target locale.
        
        URLs with other locales (e.g., /el/, /ja/) are excluded.
        URLs without locale (or matching locale) are kept.
        """
        if not locale_filter:
            return urls
        
        filtered = []
        other_locales = {'el', 'ja', 'fr', 'de', 'it', 'es', 'zh', 'ko', 'pt', 'ru', 'ar'}
        other_locales.discard(locale_filter.lower())
        
        for u in urls:
            url = u['url']
            parsed = urlparse(url)
            path = parsed.path
            
            # Check for other locale patterns in URL
            has_other_locale = False
            for other in other_locales:
                if f'/{other}/' in path.lower() or path.lower().startswith(f'/{other}/'):
                    has_other_locale = True
                    break
            
            if not has_other_locale:
                filtered.append(u)
        
        if len(filtered) < len(urls):
            print(f"    Locale filter ({locale_filter}): {len(urls)} -> {len(filtered)} URLs")
        
        return filtered
    
    def _detect_version(self, url: str) -> Optional[str]:
        """Detect documentation version from URL."""
        parsed = urlparse(url)
        path = parsed.path
        
        # Common version patterns
        patterns = [
            r'/v?(\d+\.\d+(?:\.\d+)?)',  # /3.13/, /v2.0/, /1.2.3/
            r'/(stable|latest|current|dev|main|master)/',  # /stable/, /latest/
            r'/en/(\d+\.\d+)',  # Django style: /en/5.0/
        ]
        
        for pattern in patterns:
            match = re.search(pattern, path)
            if match:
                return match.group(1)
        
        return None
    
    def _determine_scope(self, url: str) -> List[str]:
        """Determine the URL scope (path prefixes) for filtering.
        
        Returns a list of scope prefixes. For root URLs, analyzes the page
        to find documentation paths. For specific paths, returns the path prefix.
        """
        parsed = urlparse(url)
        path = parsed.path.rstrip('/')
        
        # For root URLs, analyze the page to find doc paths
        if not path or path == '/':
            doc_paths = self._analyze_documentation_paths(url)
            if doc_paths:
                return doc_paths
            return ['/']
        
        # For specific paths, return the path as scope
        return [path + '/']
    
    def _analyze_documentation_paths(self, start_url: str) -> List[str]:
        """Analyze page to find documentation path prefixes.
        
        Fetches the start page, extracts links from nav elements,
        groups by path prefix, and scores each group.
        Returns top-scoring documentation path prefixes.
        """
        try:
            response = self.session.get(start_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"  Doc path analysis failed: {e}")
            return []
        
        parsed_start = urlparse(start_url)
        base_url = f"{parsed_start.scheme}://{parsed_start.netloc}"
        
        # Find all links in navigation elements
        nav_selectors = [
            'nav', 'aside', '.sidebar', '#sidebar', '.toc', '#toc',
            '.navigation', '.nav-menu', '.docs-nav', '.doc-sidebar',
            "[role='navigation']", '.menu', '#menu', 'header', '.header'
        ]
        
        path_scores = {}
        
        for selector in nav_selectors:
            try:
                for nav in soup.select(selector):
                    for a in nav.find_all('a', href=True):
                        href = a.get('href', '')
                        full_url = self._normalize_url(href, start_url, base_url)
                        if not full_url:
                            continue
                        
                        parsed = urlparse(full_url)
                        path = parsed.path.strip('/')
                        if not path:
                            continue
                        
                        # Get first path segment
                        first_segment = path.split('/')[0]
                        if not first_segment:
                            continue
                        
                        # Score the path
                        score = 0
                        
                        # Links in nav elements get higher weight
                        score += 2
                        
                        # Doc-like paths get bonus
                        doc_patterns = ['docs', 'documentation', 'guide', 'reference', 
                                       'api', 'learn', 'tutorial', 'handbook', 'manual']
                        if any(p in first_segment.lower() for p in doc_patterns):
                            score += 3
                        
                        # Non-doc paths get penalty
                        non_doc_patterns = ['blog', 'news', 'community', 'forum', 
                                           'about', 'contact', 'pricing', 'enterprise']
                        if any(p in first_segment.lower() for p in non_doc_patterns):
                            score -= 5
                        
                        # Track score
                        prefix = '/' + first_segment + '/'
                        if prefix not in path_scores:
                            path_scores[prefix] = 0
                        path_scores[prefix] += score
            except Exception:
                continue
        
        # Return paths with positive scores, sorted by score
        positive_paths = [(p, s) for p, s in path_scores.items() if s > 0]
        positive_paths.sort(key=lambda x: x[1], reverse=True)
        
        if positive_paths:
            # Return top paths (max 5)
            return [p for p, _ in positive_paths[:5]]
        
        return []
    
    def _try_sitemap(self, base_url: str, scopes: List[str], max_pages: int, locale_filter: Optional[str] = None) -> List[Dict]:
        """Try to get URLs from sitemap."""
        parser = SitemapParser(base_url)
        
        if not parser.has_sitemap():
            return []
        
        urls = parser.parse_sitemap()
        if not urls:
            return []
        
        # Filter by scopes (OR logic - URL must match ANY scope)
        if scopes and scopes != ['/']:
            filtered_urls = []
            for u in urls:
                url = u['url']
                # Check if URL matches any scope
                parsed = urlparse(url)
                matches_scope = False
                for scope in scopes:
                    if scope in parsed.path or parsed.path.startswith(scope.rstrip('/')):
                        matches_scope = True
                        break
                if matches_scope:
                    filtered_urls.append(u)
            urls = filtered_urls
        
        # Apply locale filter
        urls = self._apply_locale_filter(urls, locale_filter)
        
        # If still too many, use LLM filtering
        if len(urls) > max_pages * 2 and self.client:
            scope_hint = scopes[0] if scopes else '/'
            urls = self._llm_filter_urls(base_url + scope_hint, urls)
        
        return urls
    
    def _try_navigation(self, start_url: str, scopes: List[str], locale_filter: Optional[str] = None) -> List[Dict]:
        """Try to extract URLs from navigation menus and SPA data."""
        try:
            response = self.session.get(start_url, timeout=30)
            response.raise_for_status()
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
        except Exception as e:
            print(f"  Navigation extraction failed: {e}")
            return []
        
        parsed_start = urlparse(start_url)
        base_url = f"{parsed_start.scheme}://{parsed_start.netloc}"
        
        urls = []
        seen = set()
        
        # 1. Try standard navigation selectors
        nav_selectors = [
            'nav', 'aside', '.sidebar', '#sidebar', '.toc', '#toc',
            '.navigation', '.nav-menu', '.docs-nav', '.doc-sidebar',
            "[role='navigation']", '.menu', '#menu'
        ]
        
        for selector in nav_selectors:
            try:
                for nav in soup.select(selector):
                    for a in nav.find_all('a', href=True):
                        href = a.get('href', '')
                        full_url = self._normalize_url(href, start_url, base_url)
                        
                        if full_url and full_url not in seen:
                            if self._url_in_scope(full_url, base_url, scopes):
                                seen.add(full_url)
                                urls.append({
                                    'url': full_url,
                                    'title': a.get_text(strip=True)[:100]
                                })
            except Exception:
                continue
        
        # 2. Try extracting from SPA data (Next.js, Docusaurus)
        if len(urls) < 5:
            spa_urls = self._extract_spa_navigation(html_content, start_url, base_url, scopes)
            for url_info in spa_urls:
                if url_info['url'] not in seen:
                    seen.add(url_info['url'])
                    urls.append(url_info)
        
        # 3. Fallback: extract from content area if still < 5 URLs
        if len(urls) < 5:
            content_urls = self._extract_content_area_links(soup, start_url, base_url, scopes, seen)
            urls.extend(content_urls)
        
        # Apply locale filter
        urls = self._apply_locale_filter(urls, locale_filter)
        
        if len(urls) > 0:
            print(f"  Navigation: found {len(urls)} URLs ({len([u for u in urls if u.get('source') == 'spa'])} from SPA data)")
        
        return urls
    
    def _extract_spa_navigation(self, html_content: str, start_url: str, base_url: str, scopes: List[str]) -> List[Dict]:
        """Extract navigation from SPA data in script tags (Next.js, Docusaurus)."""
        import re
        urls = []
        
        # Try to find __NEXT_DATA__ (Next.js)
        next_data_match = re.search(r'<script[^>]*>window\.__NEXT_DATA__\s*=\s*({.+?})</script>', html_content, re.DOTALL)
        if next_data_match:
            try:
                next_data = json.loads(next_data_match.group(1))
                # Extract page paths from Next.js data
                if 'props' in next_data and 'pageProps' in next_data['props']:
                    page_props = next_data['props']['pageProps']
                    # Look for navigation structure in various Next.js patterns
                    if 'navigation' in page_props:
                        for item in page_props['navigation']:
                            if 'url' in item:
                                full_url = self._normalize_url(item['url'], start_url, base_url)
                                if full_url and self._url_in_scope(full_url, base_url, scopes):
                                    urls.append({
                                        'url': full_url,
                                        'title': item.get('title', 'Page'),
                                        'source': 'spa'
                                    })
            except (json.JSONDecodeError, KeyError):
                pass
        
        # Try to find Docusaurus config
        docusaurus_match = re.search(r'<script[^>]*>window\.__DOCUSAURUS_CONFIG__\s*=\s*({.+?})</script>', html_content, re.DOTALL)
        if docusaurus_match:
            try:
                docusaurus_data = json.loads(docusaurus_match.group(1))
                # Docusaurus typically has themeConfig with navbar items
                if 'themeConfig' in docusaurus_data and 'navbar' in docusaurus_data['themeConfig']:
                    navbar = docusaurus_data['themeConfig']['navbar']
                    if 'items' in navbar:
                        for item in navbar['items']:
                            if 'to' in item or 'href' in item:
                                href = item.get('to') or item.get('href')
                                full_url = self._normalize_url(href, start_url, base_url)
                                if full_url and self._url_in_scope(full_url, base_url, scopes):
                                    urls.append({
                                        'url': full_url,
                                        'title': item.get('label', 'Page'),
                                        'source': 'spa'
                                    })
            except (json.JSONDecodeError, KeyError):
                pass
        
        return urls
    
    def _extract_content_area_links(self, soup, start_url: str, base_url: str, scopes: List[str], seen: set) -> List[Dict]:
        """Extract links from content area as fallback when nav selectors fail."""
        urls = []
        
        # Common content area selectors
        content_selectors = [
            'main', 'article', '.content', '#content', '.documentation',
            '.markdown', '.md-content', '[role="main"]'
        ]
        
        for selector in content_selectors:
            try:
                for content in soup.select(selector):
                    # Find all links in content area, but limit to avoid overwhelming
                    for a in content.find_all('a', href=True, limit=100):
                        href = a.get('href', '')
                        full_url = self._normalize_url(href, start_url, base_url)
                        
                        if full_url and full_url not in seen:
                            if self._url_in_scope(full_url, base_url, scopes):
                                if self._is_doc_page(full_url):
                                    seen.add(full_url)
                                    urls.append({
                                        'url': full_url,
                                        'title': a.get_text(strip=True)[:100],
                                        'source': 'content'
                                    })
                                    
                                    # Stop after finding reasonable number
                                    if len(urls) >= 50:
                                        return urls
            except Exception:
                continue
        
        return urls
    
    def _crawl_links(self, start_url: str, scopes: List[str], max_pages: int, locale_filter: Optional[str] = None) -> List[Dict]:
        """
        Crawl links within scopes, following links recursively.
        Uses BFS to discover all reachable pages matching any scope.
        """
        parsed_start = urlparse(start_url)
        base_url = f"{parsed_start.scheme}://{parsed_start.netloc}"
        
        visited = set()
        to_visit = deque([start_url])
        urls = []
        
        # Handle both single scope (backward compat) and list of scopes
        if isinstance(scopes, str):
            scopes = [scopes]
        
        scope_str = ', '.join(scopes[:3]) + ('...' if len(scopes) > 3 else '')
        print(f"  Crawling from {start_url} (scopes: {scope_str})...")
        
        while to_visit and len(urls) < max_pages:
            current_url = to_visit.popleft()
            
            if current_url in visited:
                continue
            
            visited.add(current_url)
            
            # Check locale filter before adding to results
            if locale_filter:
                test_urls = [{'url': current_url, 'title': ''}]
                filtered = self._apply_locale_filter(test_urls, locale_filter)
                if not filtered:
                    continue  # Skip URLs that don't match locale
            
            try:
                response = self.session.get(current_url, timeout=15)
                if response.status_code != 200:
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Add current page to results
                title = self._extract_title(soup, current_url)
                urls.append({'url': current_url, 'title': title})
                
                if len(urls) % 20 == 0:
                    print(f"    Crawled {len(urls)} pages, queue: {len(to_visit)}")
                
                # Find links to follow
                for a in soup.find_all('a', href=True):
                    href = a.get('href', '')
                    full_url = self._normalize_url(href, current_url, base_url)
                    
                    if full_url and full_url not in visited and full_url not in to_visit:
                        if self._url_in_scope(full_url, base_url, scopes):
                            # Skip anchors, downloads, external
                            if self._is_doc_page(full_url):
                                # Check locale before adding to queue
                                if locale_filter:
                                    test_urls = [{'url': full_url, 'title': ''}]
                                    if not self._apply_locale_filter(test_urls, locale_filter):
                                        continue  # Skip non-matching locales
                                to_visit.append(full_url)
                
            except Exception as e:
                continue
        
        print(f"    Crawl complete: {len(urls)} pages found")
        return urls
    
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
        
        # Relative URL
        return urljoin(current_url, href)
    
    def _url_in_scope(self, url: str, base_url: str, scopes: List[str]) -> bool:
        """Check if URL is within any of the defined scopes."""
        if not url.startswith(base_url):
            return False
        
        # Handle both single scope (backward compat) and list of scopes
        if isinstance(scopes, str):
            scopes = [scopes]
        
        # Check if URL matches ANY scope (OR logic)
        parsed = urlparse(url)
        for scope in scopes:
            if scope == '/':
                return True
            if scope in parsed.path or parsed.path.startswith(scope.rstrip('/')):
                return True
        
        return False
    
    def _is_doc_page(self, url: str) -> bool:
        """Check if URL looks like a documentation page."""
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        # Skip non-doc files
        skip_extensions = ['.pdf', '.zip', '.tar', '.gz', '.png', '.jpg', '.gif', '.svg', '.css', '.js']
        if any(path.endswith(ext) for ext in skip_extensions):
            return False
        
        # Skip common non-doc paths
        skip_paths = ['/search', '/login', '/logout', '/admin', '/api/', '/_', '/static/']
        if any(skip in path for skip in skip_paths):
            return False
        
        return True
    
    def _extract_title(self, soup: BeautifulSoup, url: str) -> str:
        """Extract page title from soup."""
        # Try h1
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)[:100]
        
        # Try title tag
        title = soup.find('title')
        if title:
            return title.get_text(strip=True)[:100]
        
        # Fallback to URL
        return urlparse(url).path.split('/')[-1] or 'index'
    
    def _llm_filter_urls(self, start_url: str, urls: List[Dict]) -> List[Dict]:
        """Use LLM to filter URLs intelligently."""
        if not self.client:
            return urls
        
        # Sample URLs for analysis
        sample_size = min(100, len(urls))
        step = len(urls) // sample_size
        sample_urls = [urls[i]['url'] for i in range(0, len(urls), max(1, step))][:100]
        
        parsed = urlparse(start_url)
        
        prompt = f"""Filter documentation URLs for: {start_url}

Sample URLs ({len(sample_urls)} of {len(urls)}):
{chr(10).join(sample_urls[:50])}
...
{chr(10).join(sample_urls[-20:]) if len(sample_urls) > 50 else ''}

Create substring patterns to filter relevant documentation pages.

Rules:
1. Include patterns should match the target documentation path
2. Exclude patterns should filter out: other languages, old versions, blog, downloads
3. Use simple substrings like "/en/5." or "/docs/"

Return JSON:
{{"include_patterns": ["/path/"], "exclude_patterns": ["/blog/"], "reasoning": "brief"}}"""

        try:
            response = self.client.chat.completions.create(
                model="anthropic/claude-haiku-4.5",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            result = response.choices[0].message.content.strip()
            if result.startswith("```"):
                result = re.sub(r'^```\w*\n?', '', result)
                result = re.sub(r'\n?```$', '', result)
            
            filters = json.loads(result)
            print(f"  LLM Filter: {filters.get('reasoning', '')[:60]}")
            
            # Apply filters
            include = filters.get('include_patterns', [])
            exclude = filters.get('exclude_patterns', [])
            
            filtered = []
            for u in urls:
                url = u['url']
                
                # Check excludes
                if any(p in url for p in exclude):
                    continue
                
                # Check includes
                if include and not any(p in url for p in include):
                    continue
                
                filtered.append(u)
            
            print(f"  Filtered: {len(urls)} -> {len(filtered)}")
            return filtered if filtered else urls
            
        except Exception as e:
            print(f"  LLM filter failed: {e}")
            return urls


def discover_documentation_urls(start_url: str, max_pages: int = 500) -> Dict:
    """Convenience function to discover documentation URLs."""
    discovery = URLDiscovery()
    return discovery.discover_urls(start_url, max_pages)
