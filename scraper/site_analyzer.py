import os
import re
from typing import Optional
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from models import SiteAnalysis


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
    
    def _llm_analyze(self, start_url: str, main_html: str, sample_htmls: list[str]) -> SiteAnalysis:
        soup = BeautifulSoup(main_html, 'html.parser')
        
        for script in soup(['script', 'style', 'noscript']):
            script.decompose()
        
        clean_html = str(soup)[:15000]
        
        sample_section = ""
        if sample_htmls:
            sample_soup = BeautifulSoup(sample_htmls[0], 'html.parser')
            for script in sample_soup(['script', 'style', 'noscript']):
                script.decompose()
            sample_section = f"\n\n### Sample Page HTML (first 10000 chars):\n```html\n{str(sample_soup)[:10000]}\n```"
        
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
