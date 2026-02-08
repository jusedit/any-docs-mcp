"""Unit tests for crawler.py — URL-to-filepath, title extraction."""
from crawler import Crawler
from models import EngineMode, SelectorSpec


class TestUrlToFilepath:
    def test_simple_path(self):
        assert Crawler._url_to_filepath("https://example.com/docs/intro") == "docs/intro.md"

    def test_root_url(self):
        assert Crawler._url_to_filepath("https://example.com/") == "index.md"

    def test_html_extension_stripped(self):
        assert Crawler._url_to_filepath("https://example.com/docs/page.html") == "docs/page.md"

    def test_htm_extension_stripped(self):
        assert Crawler._url_to_filepath("https://example.com/docs/page.htm") == "docs/page.md"

    def test_deep_path(self):
        result = Crawler._url_to_filepath("https://example.com/docs/api/v2/users")
        assert result == "docs/api/v2/users.md"

    def test_special_chars_sanitized(self):
        result = Crawler._url_to_filepath("https://example.com/docs/hello world?q=1")
        assert " " not in result
        assert "?" not in result


class TestExtractTitle:
    def test_h1_extracted(self):
        from bs4 import BeautifulSoup
        html = "<html><body><h1>My Title</h1><p>Content</p></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert Crawler._extract_title(soup, "fallback") == "My Title"

    def test_title_tag_fallback(self):
        from bs4 import BeautifulSoup
        html = "<html><head><title>Page Title</title></head><body><p>No h1</p></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert Crawler._extract_title(soup, "fallback") == "Page Title"

    def test_fallback_used(self):
        from bs4 import BeautifulSoup
        html = "<html><body><p>No title at all</p></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert Crawler._extract_title(soup, "My Fallback") == "My Fallback"

    def test_empty_fallback(self):
        from bs4 import BeautifulSoup
        html = "<html><body></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        assert Crawler._extract_title(soup, "") == "Untitled"
