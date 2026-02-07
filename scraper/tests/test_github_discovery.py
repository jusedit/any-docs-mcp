"""Test GitHub discovery - prefer raw markdown URLs."""
import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch
from github_discovery import GitHubDiscovery


FIXTURES_DIR = Path(__file__).parent.parent.parent / 'tests' / 'fixtures'
GITHUB_FIXTURES_DIR = FIXTURES_DIR / 'github'


def test_source_type_enum():
    """GitHubDiscovery class exists and has expected methods."""
    gd = GitHubDiscovery()
    assert hasattr(gd, 'is_github_repo')
    assert hasattr(gd, 'extract_repo_info')
    assert hasattr(gd, 'discover_markdown_files')


def test_is_github_repo_detects_valid_urls():
    """is_github_repo returns True for valid GitHub URLs."""
    gd = GitHubDiscovery()
    
    assert gd.is_github_repo('https://github.com/user/repo') is True
    assert gd.is_github_repo('https://github.com/user/repo/tree/main/docs') is True
    assert gd.is_github_repo('https://github.com/user/repo/blob/main/README.md') is True
    assert gd.is_github_repo('https://www.github.com/user/repo') is True


def test_is_github_repo_rejects_invalid_urls():
    """is_github_repo returns False for non-GitHub URLs."""
    gd = GitHubDiscovery()
    
    assert gd.is_github_repo('https://gitlab.com/user/repo') is False
    assert gd.is_github_repo('https://bitbucket.org/user/repo') is False
    assert gd.is_github_repo('https://example.com/user/repo') is False
    assert gd.is_github_repo('not-a-url') is False
    assert gd.is_github_repo('') is False


def test_extract_repo_info_simple():
    """extract_repo_info parses simple repo URLs."""
    gd = GitHubDiscovery()
    
    info = gd.extract_repo_info('https://github.com/jorgebucaran/hyperapp')
    assert info is not None
    assert info['owner'] == 'jorgebucaran'
    assert info['repo'] == 'hyperapp'
    assert info['branch'] == 'main'


def test_extract_repo_info_with_branch():
    """extract_repo_info parses URLs with explicit branch."""
    gd = GitHubDiscovery()
    
    info = gd.extract_repo_info('https://github.com/user/repo/tree/dev')
    assert info['owner'] == 'user'
    assert info['repo'] == 'repo'
    assert info['branch'] == 'dev'


def test_discover_markdown_files_uses_api():
    """discover_markdown_files returns raw GitHub URLs for markdown files."""
    gd = GitHubDiscovery()
    
    # Load the fixture
    fixture_path = GITHUB_FIXTURES_DIR / 'tree-response.json'
    with open(fixture_path, 'r') as f:
        mock_data = json.load(f)
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data
    
    with patch('github_discovery.requests.Session.get', return_value=mock_response):
        files = gd.discover_markdown_files('https://github.com/user/repo')
        
        # Should return only markdown files
        assert len(files) > 0
        for f in files:
            assert f['url'].startswith('https://raw.githubusercontent.com/')
            assert f['path'].endswith('.md')


def test_discover_markdown_files_filters_priority():
    """Markdown files in docs/ and README.md are prioritized."""
    gd = GitHubDiscovery()
    
    fixture_path = GITHUB_FIXTURES_DIR / 'tree-response.json'
    with open(fixture_path, 'r') as f:
        mock_data = json.load(f)
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data
    
    with patch('github_discovery.requests.Session.get', return_value=mock_response):
        files = gd.discover_markdown_files('https://github.com/user/repo')
        
        # First file should be README or docs file
        first_path = files[0]['path']
        assert first_path == 'README.md' or first_path.startswith('docs/')


def test_convert_blob_to_raw():
    """convert_blob_to_raw converts GitHub blob URLs to raw."""
    gd = GitHubDiscovery()
    
    blob_url = 'https://github.com/user/repo/blob/main/docs/file.md'
    raw_url = gd.convert_blob_to_raw(blob_url)
    
    assert raw_url == 'https://raw.githubusercontent.com/user/repo/main/docs/file.md'


def test_convert_already_raw_returns_unchanged():
    """convert_blob_to_raw returns raw URLs unchanged."""
    gd = GitHubDiscovery()
    
    raw_url = 'https://raw.githubusercontent.com/user/repo/main/README.md'
    result = gd.convert_blob_to_raw(raw_url)
    
    assert result == raw_url
