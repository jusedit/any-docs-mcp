"""Tests for SPA navigation extraction from captured HTML."""
import pytest
import sys
from pathlib import Path
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))

from url_discovery import URLDiscovery, ScopeRules

def _scope(base_url, prefixes):
    if isinstance(prefixes, str):
        prefixes = [prefixes]
    return ScopeRules.from_path_prefixes(base_url, prefixes)


class TestNextJSNavigation:
    """Test extracting navigation from Next.js __NEXT_DATA__."""
    
    def test_extracts_from_next_data(self):
        """Extracts navigation from __NEXT_DATA__ JSON."""
        html = """<!DOCTYPE html>
<html>
<head><title>React Docs</title></head>
<body>
    <div id="__next"></div>
    <script>window.__NEXT_DATA__ = {
        "props": {
            "pageProps": {
                "navigation": [
                    {"url": "/learn", "title": "Learn React"},
                    {"url": "/reference", "title": "API Reference"},
                    {"url": "/hooks", "title": "Hooks"}
                ]
            }
        }
    }</script>
</body>
</html>"""
        
        discovery = URLDiscovery()
        urls = discovery._extract_spa_navigation(
            html, 
            "https://react.dev/",
            "https://react.dev",
            _scope("https://react.dev", ["/"])
        )
        
        assert len(urls) == 3
        assert all(u['source'] == 'spa' for u in urls)
        assert urls[0]['url'] == 'https://react.dev/learn'
        assert urls[0]['title'] == 'Learn React'


class TestDocusaurusNavigation:
    """Test extracting navigation from Docusaurus config."""
    
    def test_extracts_from_docusaurus_config(self):
        """Extracts navigation from __DOCUSAURUS_CONFIG__."""
        html = """<!DOCTYPE html>
<html>
<head><title>Docusaurus Site</title></head>
<body>
    <div id="__docusaurus"></div>
    <script>window.__DOCUSAURUS_CONFIG__ = {
        "themeConfig": {
            "navbar": {
                "items": [
                    {"to": "/docs/intro", "label": "Introduction"},
                    {"to": "/docs/api", "label": "API"},
                    {"href": "/blog", "label": "Blog"}
                ]
            }
        }
    }</script>
</body>
</html>"""
        
        discovery = URLDiscovery()
        urls = discovery._extract_spa_navigation(
            html,
            "https://docusaurus.io/",
            "https://docusaurus.io",
            _scope("https://docusaurus.io", ["/"])
        )
        
        assert len(urls) == 3
        assert all(u['source'] == 'spa' for u in urls)


class TestContentAreaFallback:
    """Test fallback to content area link extraction."""
    
    def test_extracts_from_content_area(self):
        """Extracts links from content area when nav selectors find nothing."""
        html = """<!DOCTYPE html>
<html>
<body>
    <nav><!-- empty nav --></nav>
    <main class="content">
        <h1>Documentation</h1>
        <p>See <a href="/page1">Page One</a> for details.</p>
        <p>Also check <a href="/page2">Page Two</a>.</p>
        <p>More in <a href="/page3">Page Three</a>.</p>
    </main>
</body>
</html>"""
        
        discovery = URLDiscovery()
        soup = BeautifulSoup(html, 'html.parser')
        seen = set()
        
        urls = discovery._extract_content_area_links(
            soup,
            "https://example.com/",
            "https://example.com",
            _scope("https://example.com", ["/"]),
            seen
        )
        
        assert len(urls) >= 3
        assert all(u['source'] == 'content' for u in urls)


class TestTryNavigationIntegration:
    """Test the full _try_navigation() method with fallback chain."""
    
    def test_falls_back_to_spa_data_when_nav_empty(self):
        """Uses SPA data when standard nav selectors find nothing."""
        html = """<!DOCTYPE html>
<html>
<body>
    <!-- No standard nav elements -->
    <div class="app"></div>
    <script>window.__NEXT_DATA__ = {
        "props": {
            "pageProps": {
                "navigation": [
                    {"url": "/docs", "title": "Documentation"},
                    {"url": "/api", "title": "API"}
                ]
            }
        }
    }</script>
</body>
</html>"""
        
        discovery = URLDiscovery()
        
        # Mock the HTTP response
        class MockResponse:
            def __init__(self):
                self.text = html
            def raise_for_status(self):
                pass
        
        discovery.session = type('obj', (object,), {
            'get': lambda *args, **kwargs: MockResponse()
        })()
        
        urls = discovery._try_navigation("https://example.com/", _scope("https://example.com", ["/"]))
        
        assert len(urls) == 2
        spa_count = sum(1 for u in urls if u.get('source') == 'spa')
        assert spa_count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
