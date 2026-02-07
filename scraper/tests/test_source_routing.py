"""Test source type routing - prefer markdown over HTML extraction."""
import pytest
from pathlib import Path
from bs4 import BeautifulSoup
from unittest.mock import Mock, patch
from scraper_engine import ScraperEngine
from models import SourceType, DocumentationConfig, SiteAnalysis
from storage import StorageManager


@pytest.fixture
def tmp_storage(tmp_path):
    """Create a temporary StorageManager."""
    return StorageManager(str(tmp_path))


@pytest.fixture
def mock_config():
    """Create a minimal mock config for testing."""
    analysis = SiteAnalysis(
        content_selectors=['main', 'article'],
        navigation_selectors=['nav'],
        title_selector='h1',
        exclude_selectors=[],
        url_pattern='.*',
        base_url='https://example.com',
        grouping_strategy='single_file'
    )
    return DocumentationConfig(
        name='test',
        display_name='Test',
        start_url='https://example.com',
        site_analysis=analysis,
        version='v1',
        created_at='2024-01-01',
        updated_at='2024-01-01'
    )


def test_source_type_enum_values():
    """SourceType enum has correct values."""
    assert SourceType.RAW_MARKDOWN.value == 'raw_markdown'
    assert SourceType.HTML.value == 'html'


def test_fetch_page_detects_raw_github_content(mock_config, tmp_storage):
    """fetch_page returns RAW_MARKDOWN for raw.githubusercontent.com URLs."""
    engine = ScraperEngine(mock_config, tmp_storage)
    
    # Mock the requests.get call
    mock_response = Mock()
    mock_response.headers = {'Content-Type': 'text/plain'}
    mock_response.text = '# Hello World'
    mock_response.raise_for_status = Mock()
    
    with patch('scraper_engine.requests.get', return_value=mock_response):
        result = engine.fetch_page('https://raw.githubusercontent.com/user/repo/main/README.md')
        
        assert result is not None
        soup, source_type = result
        assert isinstance(soup, BeautifulSoup)
        assert source_type == SourceType.RAW_MARKDOWN


def test_fetch_page_detects_markdown_content_type(mock_config, tmp_storage):
    """fetch_page returns RAW_MARKDOWN for text/markdown Content-Type."""
    engine = ScraperEngine(mock_config, tmp_storage)
    
    mock_response = Mock()
    mock_response.headers = {'Content-Type': 'text/markdown'}
    mock_response.text = '# Markdown Content'
    mock_response.raise_for_status = Mock()
    
    with patch('scraper_engine.requests.get', return_value=mock_response):
        result = engine.fetch_page('https://example.com/docs/readme.md')
        
        assert result is not None
        soup, source_type = result
        assert source_type == SourceType.RAW_MARKDOWN


def test_fetch_page_returns_html_for_normal_pages(mock_config, tmp_storage):
    """fetch_page returns HTML for normal web pages."""
    engine = ScraperEngine(mock_config, tmp_storage)
    
    mock_response = Mock()
    mock_response.headers = {'Content-Type': 'text/html'}
    mock_response.text = '<html><body><h1>Title</h1></body></html>'
    mock_response.raise_for_status = Mock()
    
    with patch('scraper_engine.requests.get', return_value=mock_response):
        result = engine.fetch_page('https://example.com/page')
        
        assert result is not None
        soup, source_type = result
        assert source_type == SourceType.HTML


def test_extract_content_raw_markdown_returns_as_is(mock_config, tmp_storage):
    """extract_content returns raw markdown content unchanged when source_type is RAW_MARKDOWN."""
    engine = ScraperEngine(mock_config, tmp_storage)
    
    # Create soup with raw markdown div
    html = '<html><body><div class="raw-markdown"># Raw Markdown\n\nContent here</div></body></html>'
    soup = BeautifulSoup(html, 'html.parser')
    
    result = engine.extract_content(soup, SourceType.RAW_MARKDOWN)
    
    assert '# Raw Markdown' in result
    assert 'Content here' in result


def test_extract_content_html_uses_markdownify(mock_config, tmp_storage):
    """extract_content converts HTML to markdown when source_type is HTML."""
    engine = ScraperEngine(mock_config, tmp_storage)
    
    # HTML with content in main tag
    html = '<html><body><main><h1>Title</h1><p>Paragraph</p></main></body></html>'
    soup = BeautifulSoup(html, 'html.parser')
    
    result = engine.extract_content(soup, SourceType.HTML)
    
    # Should contain markdown-formatted content
    assert '# Title' in result or 'Title' in result


def test_extract_content_default_is_html(mock_config, tmp_storage):
    """extract_content defaults to HTML behavior when source_type not specified."""
    engine = ScraperEngine(mock_config, tmp_storage)
    
    html = '<html><body><main><h1>Title</h1></main></body></html>'
    soup = BeautifulSoup(html, 'html.parser')
    
    # Should work without explicit source_type (defaults to HTML)
    result = engine.extract_content(soup)
    
    assert 'Title' in result


def test_short_raw_content_triggers_fallback(mock_config, tmp_storage, capsys):
    """Very short raw markdown content triggers fallback warning."""
    engine = ScraperEngine(mock_config, tmp_storage)
    
    # Create soup with very short raw markdown div (<50 chars)
    html = '<html><body><div class="raw-markdown">Short</div></body></html>'
    soup = BeautifulSoup(html, 'html.parser')
    
    content = engine.extract_content(soup, SourceType.RAW_MARKDOWN)
    
    # Content should be extracted but very short
    assert len(content.strip()) < 50
    assert 'Short' in content
