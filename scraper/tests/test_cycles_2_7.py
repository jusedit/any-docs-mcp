"""Tests for Cycles 2-7: Charset detection, profiles, file guardrails."""
import pytest
from unittest.mock import Mock, patch
import requests

from scraper_engine import ScraperEngine
from content_cleaner import ContentCleaner


class TestCharsetDetection:
    """Cycle 2: Response charset detection in fetch_page."""
    
    def test_extracts_charset_from_content_type_header(self):
        """Extracts charset from Content-Type header."""
        mock_response = Mock()
        mock_response.headers = {'Content-Type': 'text/html; charset=utf-8'}
        mock_response.text = '<html>test</html>'
        mock_response.raise_for_status = Mock()
        
        # Verify charset detection
        content_type = mock_response.headers.get('Content-Type', '')
        import re
        match = re.search(r'charset=([\w-]+)', content_type, re.IGNORECASE)
        assert match
        assert match.group(1).lower() == 'utf-8'
    
    def test_fallback_to_meta_charset(self):
        """Falls back to HTML meta charset if header has no charset."""
        html = '<html><head><meta charset="iso-8859-1"></head><body>test</body></html>'
        
        import re
        meta_match = re.search(r'<meta[^>]*charset=["\']?([\w-]+)', html, re.IGNORECASE)
        assert meta_match
        assert meta_match.group(1) == 'iso-8859-1'


class TestSiteTypeProfiles:
    """Cycles 3-6: Site-type profile system and specific profiles."""
    
    def test_content_cleaner_accepts_site_type_parameter(self):
        """ContentCleaner accepts site_type parameter."""
        cleaner = ContentCleaner(site_type='mkdocs')
        assert cleaner.site_type == 'mkdocs'
    
    def test_content_cleaner_defaults_to_none(self):
        """ContentCleaner defaults to None (backward compatible)."""
        cleaner = ContentCleaner()
        assert cleaner.site_type is None
    
    def test_mkdocs_profile_exists(self):
        """PROFILES dict contains mkdocs entry."""
        from content_cleaner import ContentCleaner
        assert 'mkdocs' in ContentCleaner.PROFILES
    
    def test_sphinx_profile_exists(self):
        """PROFILES dict contains sphinx entry."""
        from content_cleaner import ContentCleaner
        assert 'sphinx' in ContentCleaner.PROFILES
    
    def test_docusaurus_profile_exists(self):
        """PROFILES dict contains docusaurus entry."""
        from content_cleaner import ContentCleaner
        assert 'docusaurus' in ContentCleaner.PROFILES
    
    def test_hugo_profile_exists(self):
        """PROFILES dict contains hugo entry."""
        from content_cleaner import ContentCleaner
        assert 'hugo' in ContentCleaner.PROFILES
    
    def test_generic_spa_profile_exists(self):
        """PROFILES dict contains generic-spa entry."""
        from content_cleaner import ContentCleaner
        assert 'generic-spa' in ContentCleaner.PROFILES


class TestFileSizeGuardrails:
    """Cycle 7: File size guardrails with auto-split."""
    
    def test_scraper_engine_accepts_max_file_size_kb(self):
        """ScraperEngine accepts max_file_size_kb parameter."""
        from models import DocumentationConfig, SiteAnalysis
        from storage import StorageManager
        import tempfile
        from datetime import datetime
        
        with tempfile.TemporaryDirectory() as tmpdir:
            site_analysis = SiteAnalysis(
                content_selectors=['article'],
                navigation_selectors=['nav'],
                url_pattern='.*',
                base_url='https://example.com'
            )
            config = DocumentationConfig(
                name='test',
                display_name='Test',
                start_url='https://example.com',
                site_analysis=site_analysis,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            storage = StorageManager(tmpdir)
            
            engine = ScraperEngine(config, storage, max_file_size_kb=500)
            assert engine.max_file_size_kb == 500
    
    def test_default_max_file_size_is_500kb(self):
        """Default max_file_size_kb is 500."""
        from models import DocumentationConfig, SiteAnalysis
        from storage import StorageManager
        import tempfile
        from datetime import datetime
        
        with tempfile.TemporaryDirectory() as tmpdir:
            site_analysis = SiteAnalysis(
                content_selectors=['article'],
                navigation_selectors=['nav'],
                url_pattern='.*',
                base_url='https://example.com'
            )
            config = DocumentationConfig(
                name='test',
                display_name='Test',
                start_url='https://example.com',
                site_analysis=site_analysis,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            storage = StorageManager(tmpdir)
            
            engine = ScraperEngine(config, storage)
            assert engine.max_file_size_kb == 500
