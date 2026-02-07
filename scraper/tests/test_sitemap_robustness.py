"""Tests for SitemapParser edge cases and robustness."""
import gzip
import pytest
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))

from sitemap_parser import SitemapParser


class TestSitemapIndexHandling:
    """Test sitemap index files (sitemapindex → multiple sitemaps)."""
    
    def test_parses_sitemap_index(self, tmp_path):
        """Handles sitemap index files with multiple sub-sitemaps."""
        # Create mock sitemap index
        index_content = b"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <sitemap>
        <loc>https://example.com/sitemap1.xml</loc>
    </sitemap>
    <sitemap>
        <loc>https://example.com/sitemap2.xml</loc>
    </sitemap>
</sitemapindex>"""
        
        # Create mock sub-sitemap
        sub_content = b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>https://example.com/page1</loc></url>
    <url><loc>https://example.com/page2</loc></url>
</urlset>"""
        
        parser = SitemapParser("https://example.com")
        
        with patch('requests.get') as mock_get:
            # First call returns index, subsequent calls return sub-sitemaps
            mock_get.side_effect = [
                Mock(content=index_content, headers={}, status_code=200, raise_for_status=lambda: None),
                Mock(content=sub_content, headers={}, status_code=200, raise_for_status=lambda: None),
                Mock(content=sub_content, headers={}, status_code=200, raise_for_status=lambda: None),
            ]
            
            links = parser._parse_sitemap_file("https://example.com/sitemap.xml")
            
            # Should get 4 URLs (2 from each sub-sitemap)
            assert len(links) == 4
            assert all(l['url'].startswith('https://example.com/') for l in links)


class TestGzippedSitemaps:
    """Test handling of .xml.gz compressed sitemaps."""
    
    def test_parses_gzipped_sitemap(self):
        """Handles gzipped sitemap files."""
        # Create gzipped sitemap content
        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>https://example.com/page1</loc></url>
    <url><loc>https://example.com/page2</loc></url>
</urlset>"""
        gzipped = gzip.compress(xml_content)
        
        parser = SitemapParser("https://example.com")
        
        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(
                content=gzipped,
                headers={'content-type': 'application/gzip'},
                status_code=200,
                raise_for_status=lambda: None
            )
            
            links = parser._parse_sitemap_file("https://example.com/sitemap.xml.gz")
            
            assert len(links) == 2
            assert links[0]['url'] == 'https://example.com/page1'


class TestLastmodFiltering:
    """Test filtering by lastmod date."""
    
    def test_filters_by_lastmod_date(self):
        """Only returns URLs with lastmod > refresh_after date."""
        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://example.com/recent</loc>
        <lastmod>2024-06-15</lastmod>
    </url>
    <url>
        <loc>https://example.com/old</loc>
        <lastmod>2023-01-01</lastmod>
    </url>
    <url>
        <loc>https://example.com/nodate</loc>
    </url>
</urlset>"""
        
        parser = SitemapParser("https://example.com")
        
        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(
                content=xml_content,
                headers={},
                status_code=200,
                raise_for_status=lambda: None
            )
            
            # Only want URLs modified after 2024-01-01
            refresh_date = datetime(2024, 1, 1)
            links = parser._parse_sitemap_file("https://example.com/sitemap.xml", refresh_after=refresh_date)
            
            # Should get recent page and page without date
            assert len(links) == 2
            urls = [l['url'] for l in links]
            assert 'https://example.com/recent' in urls
            assert 'https://example.com/nodate' in urls
            assert 'https://example.com/old' not in urls


class TestRobotsTxtDiscovery:
    """Test discovering sitemap from robots.txt."""
    
    def test_discovers_sitemap_from_robots_txt(self):
        """Parses Sitemap: directive from robots.txt."""
        robots_content = """User-agent: *
Allow: /
Sitemap: https://example.com/custom-sitemap.xml
Sitemap: https://example.com/another-sitemap.xml
"""
        
        parser = SitemapParser("https://example.com")
        
        with patch('requests.get') as mock_get:
            with patch.object(parser, '_check_url_exists', return_value=False):
                mock_get.return_value = Mock(
                    text=robots_content,
                    status_code=200
                )
                
                urls = parser._parse_robots_txt()
                
                assert len(urls) == 2
                assert 'https://example.com/custom-sitemap.xml' in urls
                assert 'https://example.com/another-sitemap.xml' in urls
    
    def test_discover_sitemap_urls_uses_robots_txt(self):
        """discover_sitemap_urls() includes sitemaps from robots.txt."""
        robots_content = "Sitemap: https://example.com/robots-sitemap.xml\n"
        
        parser = SitemapParser("https://example.com")
        
        with patch('requests.get') as mock_get:
            # robots.txt exists and has sitemap
            mock_get.return_value = Mock(text=robots_content, status_code=200)
            
            with patch.object(parser, '_check_url_exists', return_value=False):
                urls = parser.discover_sitemap_urls()
                
                assert 'https://example.com/robots-sitemap.xml' in urls


class TestGracefulErrors:
    """Test graceful handling of errors."""
    
    def test_returns_empty_list_for_404(self):
        """Gracefully returns empty list when sitemap 404s."""
        parser = SitemapParser("https://example.com")
        
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("404 Not Found")
            
            links = parser._parse_sitemap_file("https://example.com/sitemap.xml")
            
            assert links == []
    
    def test_returns_empty_list_for_invalid_xml(self):
        """Gracefully handles invalid XML."""
        parser = SitemapParser("https://example.com")
        
        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(
                content=b"Not valid XML",
                headers={},
                status_code=200,
                raise_for_status=lambda: None
            )
            
            links = parser._parse_sitemap_file("https://example.com/sitemap.xml")
            
            assert links == []
    
    def test_has_sitemap_returns_false_when_no_sitemap(self):
        """has_sitemap() returns False when no sitemap exists."""
        parser = SitemapParser("https://example.com")
        
        with patch.object(parser, '_check_url_exists', return_value=False):
            with patch.object(parser, '_parse_robots_txt', return_value=[]):
                assert parser.has_sitemap() is False
    
    def test_has_sitemap_returns_true_when_robots_has_sitemap(self):
        """has_sitemap() returns True when robots.txt has Sitemap:."""
        parser = SitemapParser("https://example.com")
        
        with patch.object(parser, '_check_url_exists', return_value=False):
            with patch.object(parser, '_parse_robots_txt', return_value=['https://example.com/sitemap.xml']):
                assert parser.has_sitemap() is True


class TestStandardLocations:
    """Test checking standard sitemap locations."""
    
    def test_checks_sitemap_xml(self):
        """Discovers sitemap at /sitemap.xml."""
        parser = SitemapParser("https://example.com")
        
        with patch.object(parser, '_check_url_exists') as mock_check:
            mock_check.side_effect = lambda url: url.endswith('/sitemap.xml')
            
            urls = parser.discover_sitemap_urls()
            
            assert 'https://example.com/sitemap.xml' in urls
    
    def test_checks_sitemap_index_xml(self):
        """Discovers sitemap at /sitemap-index.xml."""
        parser = SitemapParser("https://example.com")
        
        with patch.object(parser, '_check_url_exists') as mock_check:
            # sitemap.xml doesn't exist, but sitemap-index.xml does
            mock_check.side_effect = lambda url: 'sitemap-index' in url
            
            urls = parser.discover_sitemap_urls()
            
            assert 'https://example.com/sitemap-index.xml' in urls


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
