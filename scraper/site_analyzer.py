import os
import re
import json
from typing import Optional, List, Dict
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from models import SiteAnalysis

# Load .env from parent directory if present
from dotenv import load_dotenv
import os as os_module
load_dotenv(os_module.path.join(os_module.path.dirname(__file__), '..', '.env'))


class SiteAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key required. Set OPENROUTER_API_KEY environment variable.")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )
    
    def fetch_page_html(self, url: str) -> str:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    
    def analyze_site(self, start_url: str, sample_urls: Optional[list[str]] = None) -> SiteAnalysis:
        print(f"Analyzing documentation site: {start_url}")
        
        main_html = self.fetch_page_html(start_url)
        soup = BeautifulSoup(main_html, 'html.parser')
        
        sample_htmls = []
        if sample_urls:
            print(f"Fetching {len(sample_urls)} sample pages for analysis...")
            for url in sample_urls[:3]:
                try:
                    sample_htmls.append(self.fetch_page_html(url))
                except Exception as e:
                    print(f"  Warning: Could not fetch {url}: {e}")
        
        print("Sending to LLM for analysis...")
        analysis = self._llm_analyze(start_url, main_html, sample_htmls)
        
        return analysis
    
    def _sanitize_html_for_prompt(self, html: str) -> str:
        """Sanitize HTML to prevent prompt injection attacks."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove potentially dangerous tags
        for tag in soup(['script', 'style', 'noscript', 'iframe', 'object', 'embed']):
            tag.decompose()
        
        # Get text content and limit size
        text = str(soup)[:15000]
        
        # Escape prompt injection attempts
        text = text.replace('"""', '\'\'\'')  # Prevent breaking out of prompt
        text = text.replace('```', '\'\'\'')  # Prevent code block injection
        
        return text
    
    def _llm_analyze(self, start_url: str, main_html: str, sample_htmls: list[str]) -> SiteAnalysis:
        clean_html = self._sanitize_html_for_prompt(main_html)
        
        sample_section = ""
        if sample_htmls:
            sample_clean = self._sanitize_html_for_prompt(sample_htmls[0])
            sample_section = f"\n\n### Sample Page HTML (first 10000 chars):\n{sample_clean[:10000]}"
        
        prompt = f"""You are analyzing a documentation website to extract content programmatically.

**Start URL:** {start_url}

**Main Page HTML (first 15000 chars):**
```html
{clean_html}
```
{sample_section}

Analyze this HTML and provide extraction rules as JSON following this schema:

{{
  "content_selectors": ["CSS selector for main content, in priority order"],
  "navigation_selectors": ["CSS selectors for navigation/sidebar menu"],
  "title_selector": "CSS selector for page title (optional)",
  "exclude_selectors": ["CSS selectors for elements to remove like headers, footers, TOC"],
  "url_pattern": "regex pattern to match valid documentation URLs",
  "base_url": "base URL (protocol + domain)",
  "grouping_strategy": "path_depth_2 or path_depth_3 or single_file",
  "notes": "brief notes about the site structure"
}}

**Guidelines:**
1. content_selectors: Look for main article/content container (e.g., "main.content", ".documentation", "#main-content")
2. navigation_selectors: Find sidebar or navigation menu with links to all docs
3. exclude_selectors: Identify headers, footers, TOC, breadcrumbs, "edit this page" links, etc.
4. url_pattern: Create regex to match only documentation pages (e.g., "https://example\\.com/docs/.*")
5. grouping_strategy: Use "path_depth_2" for sites with /category/page structure, "path_depth_3" for deeper hierarchies
6. Be specific with CSS selectors - use IDs and classes visible in the HTML

Return ONLY valid JSON, no other text."""

        response = self.client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        result_text = response.choices[0].message.content.strip()
        
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        result_text = result_text.strip()
        
        import json
        analysis_dict = json.loads(result_text)
        
        return SiteAnalysis(**analysis_dict)
    
    def discover_navigation_links(self, start_url: str, nav_selectors: list[str]) -> list[dict]:
        html = self.fetch_page_html(start_url)
        soup = BeautifulSoup(html, 'html.parser')
        
        links = []
        seen_urls = set()
        
        for selector in nav_selectors:
            nav_element = soup.select_one(selector)
            if nav_element:
                for a in nav_element.find_all('a', href=True):
                    href = a.get('href', '')
                    
                    if href.startswith('#'):
                        continue
                    
                    from urllib.parse import urljoin
                    full_url = urljoin(start_url, href)
                    full_url = full_url.split('#')[0]
                    
                    if full_url not in seen_urls:
                        seen_urls.add(full_url)
                        title = a.get_text(strip=True)
                        links.append({'url': full_url, 'title': title})
                
                break
        
        return links
    
    def filter_sitemap_urls(self, start_url: str, sitemap_urls: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Use LLM to intelligently filter sitemap URLs to only include relevant documentation pages.
        Excludes: blog posts, release notes, other languages, old versions, etc.
        """
        if len(sitemap_urls) <= 50:
            # Small sitemap, no need to filter
            return sitemap_urls
        
        # Sample URLs for LLM analysis
        sample_size = min(100, len(sitemap_urls))
        step = len(sitemap_urls) // sample_size
        sample_urls = [sitemap_urls[i]['url'] for i in range(0, len(sitemap_urls), max(1, step))][:100]
        
        parsed_start = urlparse(start_url)
        start_path = parsed_start.path.rstrip('/')
        
        prompt = f"""You are filtering a sitemap to find only relevant documentation URLs.

**Target Documentation:** {start_url}
**Start Path:** {start_path}
**Total URLs in Sitemap:** {len(sitemap_urls)}

**Sample URLs from Sitemap (showing {len(sample_urls)} of {len(sitemap_urls)}):**
{chr(10).join(sample_urls[:50])}
{'...' if len(sample_urls) > 50 else ''}
{chr(10).join(sample_urls[-20:]) if len(sample_urls) > 50 else ''}

Create SIMPLE string patterns to filter URLs. The patterns will be used with Python `in` operator (substring match).

**CRITICAL RULES:**
1. Use SIMPLE substring patterns like "/docs/" or "/api/" - NOT regex
2. If start_url has a language code like "/en/", the include pattern MUST contain that language
3. If start_url has a version like "/stable/" or "/current/", include that OR the latest version number
4. Keep patterns as LITERAL SUBSTRINGS that must appear in the URL

**EXAMPLES:**
- Start URL: https://docs.djangoproject.com/en/stable/
  → include_patterns: ["/en/5.", "/en/stable/"] (English + latest version)
  → exclude_patterns: ["/de/", "/fr/", "/ja/", "/es/", "/pt/", "/ko/", "/zh/"]

- Start URL: https://nodejs.org/api/
  → include_patterns: ["/api/"]
  → exclude_patterns: ["/blog/", "/learn/"]

- Start URL: https://kubernetes.io/docs/home/
  → include_patterns: ["/docs/"]
  → exclude_patterns: ["/blog/", "/zh/", "/ko/", "/ja/", "/de/", "/fr/"]

Return JSON:
{{
  "include_patterns": ["/path/substring/"],
  "exclude_patterns": ["/blog/", "/other-lang/"],
  "reasoning": "brief explanation"
}}

Return ONLY valid JSON, no markdown."""

        try:
            response = self.client.chat.completions.create(
                model="anthropic/claude-haiku-4.5",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1000
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Clean JSON
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            try:
                filters = json.loads(result_text)
                print(f"  LLM URL Filter: {filters.get('reasoning', 'No reasoning')}")
            except json.JSONDecodeError as e:
                print(f"  Warning: Failed to parse LLM response as JSON: {e}")
                return sitemap_urls
            
            # Apply filters using simple substring matching
            filtered = []
            include_patterns = filters.get('include_patterns', [])
            exclude_patterns = filters.get('exclude_patterns', [])
            
            for url_dict in sitemap_urls:
                url = url_dict['url']
                
                # Check excludes first (substring match)
                excluded = False
                for pattern in exclude_patterns:
                    if pattern in url:
                        excluded = True
                        break
                
                if excluded:
                    continue
                
                # Check includes (if any patterns specified, URL must match at least one)
                if include_patterns:
                    included = False
                    for pattern in include_patterns:
                        if pattern in url:
                            included = True
                            break
                    if not included:
                        continue
                
                filtered.append(url_dict)
            
            print(f"  Filtered {len(sitemap_urls)} -> {len(filtered)} URLs")
            
            # If filter removed too many (>95%) or left too few, use path-based fallback
            if len(filtered) < 10:
                print(f"  Warning: Filter too aggressive ({len(filtered)} URLs), using path-based fallback")
                # Fallback: filter by start_path
                if start_path:
                    filtered = [u for u in sitemap_urls if f'/{start_path}' in u['url'] or u['url'].endswith(f'/{start_path}')]
                    print(f"  Path fallback: {len(filtered)} URLs matching '/{start_path}'")
                
                # If still too few, try the full start URL path
                if len(filtered) < 10:
                    full_path = parsed_start.path.rstrip('/')
                    if full_path and full_path != f'/{start_path}':
                        filtered = [u for u in sitemap_urls if full_path in u['url']]
                        print(f"  Full path fallback: {len(filtered)} URLs matching '{full_path}'")
                
                if not filtered:
                    return sitemap_urls
            
            return filtered
            
        except Exception as e:
            print(f"  Warning: LLM URL filtering failed: {e}")
            return sitemap_urls  # Return unfiltered on error
