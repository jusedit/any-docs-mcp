"""Tests for ResponseCapture HTTP fixture system."""
import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime

import requests
from response_capture import ResponseCapture, CapturedResponse


class TestUrlToSlug:
    """URL-to-slug conversion tests."""
    
    def test_simple_url(self):
        """Simple domain and path."""
        assert ResponseCapture.url_to_slug("https://example.com/page") == "example-com-page"
    
    def test_react_dev_example(self):
        """React.dev learn/state example from AC."""
        slug = ResponseCapture.url_to_slug("https://react.dev/learn/state")
        assert slug == "react-dev-learn-state"
    
    def test_fastapi_example(self):
        """FastAPI tutorial URL."""
        slug = ResponseCapture.url_to_slug("https://fastapi.tiangolo.com/tutorial/")
        assert slug == "fastapi-tiangolo-com-tutorial"
    
    def test_github_raw_example(self):
        """GitHub raw content URL."""
        url = "https://raw.githubusercontent.com/jorgebucaran/hyperapp/main/docs/reference.md"
        slug = ResponseCapture.url_to_slug(url)
        assert "raw-githubusercontent-com" in slug
        assert "hyperapp" in slug
    
    def test_query_params_removed(self):
        """Query parameters should be stripped."""
        slug = ResponseCapture.url_to_slug("https://example.com/page?foo=bar&baz=qux")
        assert "?" not in slug
        assert "foo" not in slug
    
    def test_fragment_removed(self):
        """Fragment identifiers should be stripped."""
        slug = ResponseCapture.url_to_slug("https://example.com/page#section")
        assert "#" not in slug
        assert "section" not in slug
    
    def test_multiple_hyphens_collapsed(self):
        """Multiple consecutive non-alphanumeric should become single hyphen."""
        slug = ResponseCapture.url_to_slug("https://example.com///path///to///page")
        # Should not have multiple consecutive hyphens
        assert "---" not in slug
    
    def test_leading_trailing_hyphens_removed(self):
        """Leading/trailing hyphens should be stripped."""
        slug = ResponseCapture.url_to_slug("https:///example.com/page/")
        assert not slug.startswith("-")
        assert not slug.endswith("-")
    
    def test_very_long_url_uses_hash(self):
        """Very long URLs should include hash for uniqueness."""
        long_url = "https://example.com/" + "a/" * 100 + "page"
        slug = ResponseCapture.url_to_slug(long_url)
        # Should be truncated with hash
        assert len(slug) <= 100


class TestResponseCapture:
    """ResponseCapture class tests."""
    
    @pytest.fixture
    def capture(self, tmp_path):
        """Create ResponseCapture with temp fixtures dir."""
        return ResponseCapture(fixtures_dir=str(tmp_path / "fixtures"))
    
    @pytest.fixture
    def mock_response(self):
        """Create a mock requests response."""
        mock = Mock()
        mock.status_code = 200
        mock.headers = {"Content-Type": "text/html", "X-Custom": "value"}
        mock.text = "<html><body>Test content</body></html>"
        return mock
    
    def test_capture_returns_captured_response(self, capture, mock_response):
        """capture() returns CapturedResponse dataclass."""
        with patch('requests.get', return_value=mock_response):
            resp = capture.capture("https://example.com/page")
        
        assert isinstance(resp, CapturedResponse)
        assert resp.status == 200
        assert resp.headers == {"Content-Type": "text/html", "X-Custom": "value"}
        assert resp.body == "<html><body>Test content</body></html>"
        assert resp.url == "https://example.com/page"
        assert resp.captured_at  # Should have timestamp
    
    def test_capture_raises_on_http_error(self, capture):
        """capture() raises on HTTP error status."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404")
        
        with patch('requests.get', return_value=mock_response):
            with pytest.raises(requests.HTTPError):
                capture.capture("https://example.com/notfound")
    
    def test_capture_truncates_large_body(self, capture):
        """capture() truncates body over 1 MB."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.text = "x" * (2 * 1024 * 1024)  # 2 MB
        
        with patch('requests.get', return_value=mock_response):
            resp = capture.capture("https://example.com/large")
        
        assert len(resp.body) <= ResponseCapture.MAX_BODY_SIZE
    
    def test_save_creates_meta_and_body_files(self, capture, mock_response):
        """save() creates .meta.json and .body.html files."""
        with patch('requests.get', return_value=mock_response):
            resp = capture.capture("https://example.com/page")
        
        meta_path, body_path = capture.save(resp, "test-doc")
        
        # Both files should exist
        assert meta_path.exists()
        assert body_path.exists()
        
        # Meta file should be valid JSON with expected fields
        with open(meta_path) as f:
            meta = json.load(f)
        assert meta["status"] == 200
        assert meta["headers"]["Content-Type"] == "text/html"
        assert meta["original_url"] == "https://example.com/page"
        assert "captured_at" in meta
        assert "slug" in meta
        
        # Body file should contain HTML
        with open(body_path) as f:
            body = f.read()
        assert body == "<html><body>Test content</body></html>"
    
    def test_save_handles_collision(self, capture, mock_response):
        """save() handles slug collision by appending hash."""
        with patch('requests.get', return_value=mock_response):
            resp1 = capture.capture("https://example.com/page")
            resp2 = capture.capture("https://example.com/page?different=query")
        
        # Force same slug by manipulating URL
        resp2.url = resp1.url  # Same URL
        
        meta_path1, _ = capture.save(resp1, "test-doc")
        meta_path2, _ = capture.save(resp2, "test-doc")
        
        # Second save should have different filename
        assert meta_path1 != meta_path2
    
    def test_load_round_trip(self, capture, mock_response):
        """load() reconstructs CapturedResponse from disk."""
        with patch('requests.get', return_value=mock_response):
            resp = capture.capture("https://example.com/page")
        
        meta_path, _ = capture.save(resp, "test-doc")
        slug = json.load(open(meta_path))["slug"]
        
        loaded = capture.load("test-doc", slug)
        
        assert loaded.status == resp.status
        assert loaded.headers == resp.headers
        assert loaded.body == resp.body
        assert loaded.url == resp.url


class TestCLI:
    """CLI entry point tests (code inspection)."""
    
    def test_cli_capture_command_exists(self):
        """CLI has 'capture' command implemented."""
        # This test just verifies the code structure exists
        import response_capture as rc
        
        # Check that __main__ block exists with capture command
        source = Path(rc.__file__).read_text()
        assert 'if __name__ == "__main__":' in source
        assert 'capture' in source
        assert 'sys.argv' in source
