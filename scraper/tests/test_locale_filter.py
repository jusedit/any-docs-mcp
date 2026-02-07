"""Tests for URL Discovery locale filter functionality."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from url_discovery import URLDiscovery, discover_documentation_urls


class TestLocaleDetection:
    """Test _detect_locale() method."""
    
    def test_detects_en_from_django_style_url(self):
        """Detects 'en' from /en/stable/ URL pattern."""
        discovery = URLDiscovery()
        result = discovery._detect_locale("https://docs.djangoproject.com/en/stable/")
        assert result == "en"
    
    def test_detects_de_from_german_url(self):
        """Detects 'de' from /de/ URL pattern."""
        discovery = URLDiscovery()
        result = discovery._detect_locale("https://example.com/de/docs/")
        assert result == "de"
    
    def test_detects_el_from_greek_url(self):
        """Detects 'el' from /el/ URL pattern (Greek)."""
        discovery = URLDiscovery()
        result = discovery._detect_locale("https://docs.djangoproject.com/el/5.0/")
        assert result == "el"
    
    def test_returns_none_for_docs_path(self):
        """Returns None for /docs/ path (not a locale)."""
        discovery = URLDiscovery()
        result = discovery._detect_locale("https://react.dev/docs/")
        assert result is None
    
    def test_returns_none_for_api_path(self):
        """Returns None for /api/ path (not a locale)."""
        discovery = URLDiscovery()
        result = discovery._detect_locale("https://api.example.com/api/v1/")
        assert result is None
    
    def test_detects_ja_from_japanese_url(self):
        """Detects 'ja' from /ja/ URL pattern."""
        discovery = URLDiscovery()
        result = discovery._detect_locale("https://docs.python.org/ja/3/")
        assert result == "ja"


class TestLocaleFilter:
    """Test _apply_locale_filter() method."""
    
    def test_filters_out_el_urls_when_en_filter(self):
        """Excludes Greek URLs when locale_filter='en'."""
        discovery = URLDiscovery()
        urls = [
            {"url": "https://docs.djangoproject.com/en/stable/intro/", "title": "English"},
            {"url": "https://docs.djangoproject.com/el/5.0/intro/", "title": "Greek"},
            {"url": "https://docs.djangoproject.com/ja/stable/intro/", "title": "Japanese"},
        ]
        result = discovery._apply_locale_filter(urls, "en")
        assert len(result) == 1
        assert result[0]["url"] == "https://docs.djangoproject.com/en/stable/intro/"
    
    def test_keeps_all_urls_when_no_filter(self):
        """Keeps all URLs when locale_filter is None."""
        discovery = URLDiscovery()
        urls = [
            {"url": "https://docs.djangoproject.com/en/stable/intro/", "title": "English"},
            {"url": "https://docs.djangoproject.com/el/5.0/intro/", "title": "Greek"},
        ]
        result = discovery._apply_locale_filter(urls, None)
        assert len(result) == 2
    
    def test_filters_out_fr_urls_when_de_filter(self):
        """Excludes non-German URLs when locale_filter='de'."""
        discovery = URLDiscovery()
        urls = [
            {"url": "https://example.com/de/docs/", "title": "German"},
            {"url": "https://example.com/fr/docs/", "title": "French"},
            {"url": "https://example.com/en/docs/", "title": "English"},
        ]
        result = discovery._apply_locale_filter(urls, "de")
        # Should keep only German, exclude French and English (both are non-de locales)
        assert len(result) == 1
        urls_in_result = [u["url"] for u in result]
        assert "https://example.com/de/docs/" in urls_in_result
        assert "https://example.com/fr/docs/" not in urls_in_result
        assert "https://example.com/en/docs/" not in urls_in_result


class TestDiscoverUrlsLocaleParameter:
    """Test discover_urls() accepts and uses locale_filter parameter."""
    
    def test_accepts_locale_filter_parameter(self):
        """discover_urls() accepts optional locale_filter parameter."""
        discovery = URLDiscovery()
        # Should not raise TypeError
        result = discovery.discover_urls(
            "https://docs.djangoproject.com/en/stable/",
            max_pages=10,
            locale_filter="en"
        )
        assert "locale" in result
        assert result["locale"] == "en"
    
    def test_auto_detects_locale_from_start_url(self):
        """Auto-detects locale from start_url when not provided."""
        discovery = URLDiscovery()
        result = discovery.discover_urls(
            "https://docs.djangoproject.com/en/stable/",
            max_pages=10
        )
        assert result["locale"] == "en"


class TestDjangoSitemapLocaleFilter:
    """Test locale filtering with Django-style multi-locale sitemap."""
    
    def test_mock_sitemap_with_multiple_locales(self, tmp_path):
        """Filters Django sitemap with /en/, /el/, /ja/ URLs."""
        discovery = URLDiscovery()
        
        # Create mock sitemap fixture
        sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://docs.djangoproject.com/en/stable/intro/</loc>
    </url>
    <url>
        <loc>https://docs.djangoproject.com/el/5.0/intro/</loc>
    </url>
    <url>
        <loc>https://docs.djangoproject.com/ja/stable/intro/</loc>
    </url>
    <url>
        <loc>https://docs.djangoproject.com/en/stable/topics/</loc>
    </url>
</urlset>"""
        
        # Mock the sitemap parser to return parsed URLs
        urls = [
            {"url": "https://docs.djangoproject.com/en/stable/intro/", "title": ""},
            {"url": "https://docs.djangoproject.com/el/5.0/intro/", "title": ""},
            {"url": "https://docs.djangoproject.com/ja/stable/intro/", "title": ""},
            {"url": "https://docs.djangoproject.com/en/stable/topics/", "title": ""},
        ]
        
        # Apply locale filter
        result = discovery._apply_locale_filter(urls, "en")
        
        # Should only have English URLs
        assert len(result) == 2
        for u in result:
            assert "/en/" in u["url"]
            assert "/el/" not in u["url"]
            assert "/ja/" not in u["url"]


class TestConvenienceFunction:
    """Test that discover_documentation_urls() still works (backward compat)."""
    
    def test_convenience_function_works_without_locale_filter(self):
        """Backward compatibility: function works without locale_filter."""
        # This test may fail if no network, but verifies the API still works
        try:
            result = discover_documentation_urls("https://react.dev/learn/", max_pages=5)
            assert "urls" in result
            assert "mode" in result
        except Exception as e:
            # Network error is acceptable for this test
            if "Connection" in str(e) or "Timeout" in str(e):
                pytest.skip("Network not available")
            raise


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
