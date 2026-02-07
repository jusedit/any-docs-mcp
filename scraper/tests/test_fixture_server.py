"""Tests for FixtureHTTPServer mock server."""
import pytest
import requests
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from scraper.tests.fixture_server import FixtureHTTPServer


class TestFixtureHTTPServer:
    """Tests for FixtureHTTPServer functionality."""
    
    @pytest.fixture
    def sample_fixture(self, tmp_path):
        """Create a sample fixture file for testing."""
        fixtures_dir = tmp_path / "fixtures"
        doc_dir = fixtures_dir / "test-doc"
        doc_dir.mkdir(parents=True)
        
        # Create meta file
        meta = {
            "status": 200,
            "headers": {"Content-Type": "text/html"},
            "original_url": "https://example.com/page",
            "captured_at": "2024-01-01T00:00:00Z",
            "slug": "example-com-page"
        }
        with open(doc_dir / "example-com-page.meta.json", 'w') as f:
            json.dump(meta, f)
        
        # Create body file
        with open(doc_dir / "example-com-page.body.html", 'w') as f:
            f.write("<html><body>Test content</body></html>")
        
        return fixtures_dir
    
    def test_start_returns_base_url(self, sample_fixture):
        """start() returns a working base URL."""
        server = FixtureHTTPServer(fixtures_dir=str(sample_fixture))
        base_url = server.start()
        
        assert base_url.startswith("http://localhost:")
        assert server.port is not None
        assert server.port > 0
        
        server.stop()
    
    def test_get_returns_fixture_content(self, sample_fixture):
        """GET request returns fixture body content."""
        server = FixtureHTTPServer(fixtures_dir=str(sample_fixture))
        base_url = server.start()
        
        try:
            response = requests.get(f"{base_url}/test-doc/example-com-page")
            assert response.status_code == 200
            assert "Test content" in response.text
            assert response.headers['Content-Type'] == 'text/html'
        finally:
            server.stop()
    
    def test_get_returns_404_for_missing_fixture(self, sample_fixture):
        """GET request for non-existent fixture returns 404."""
        server = FixtureHTTPServer(fixtures_dir=str(sample_fixture))
        base_url = server.start()
        
        try:
            response = requests.get(f"{base_url}/test-doc/non-existent")
            assert response.status_code == 404
        finally:
            server.stop()
    
    def test_get_returns_404_for_missing_doc_dir(self, sample_fixture):
        """GET request for non-existent doc directory returns 404."""
        server = FixtureHTTPServer(fixtures_dir=str(sample_fixture))
        base_url = server.start()
        
        try:
            response = requests.get(f"{base_url}/non-existent/page")
            assert response.status_code == 404
        finally:
            server.stop()
    
    def test_concurrent_requests(self, sample_fixture):
        """Server handles concurrent requests without deadlock."""
        server = FixtureHTTPServer(fixtures_dir=str(sample_fixture))
        base_url = server.start()
        
        try:
            # Send 10 parallel requests
            urls = [f"{base_url}/test-doc/example-com-page"] * 10
            
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(requests.get, url) for url in urls]
                responses = [f.result() for f in as_completed(futures)]
            
            # All should succeed
            assert all(r.status_code == 200 for r in responses)
            assert all("Test content" in r.text for r in responses)
        finally:
            server.stop()
    
    def test_get_rewritten_url_converts_original(self, sample_fixture):
        """get_rewritten_url() converts original URL to localhost."""
        server = FixtureHTTPServer(fixtures_dir=str(sample_fixture))
        server.start()
        
        try:
            # Create a fixture for react.dev
            doc_dir = Path(sample_fixture) / "react-dev"
            doc_dir.mkdir()
            meta = {
                "status": 200,
                "headers": {},
                "original_url": "https://react.dev/learn/state",
                "slug": "react-dev-learn-state"
            }
            with open(doc_dir / "react-dev-learn-state.meta.json", 'w') as f:
                json.dump(meta, f)
            with open(doc_dir / "react-dev-learn-state.body.html", 'w') as f:
                f.write("<html>React State</html>")
            
            # Test URL rewriting
            rewritten = server.get_rewritten_url("https://react.dev/learn/state")
            assert rewritten.startswith(server.base_url)
            assert "/react/learn-state" in rewritten
        finally:
            server.stop()
    
    def test_get_rewritten_url_raises_if_not_started(self, sample_fixture):
        """get_rewritten_url() raises if server not started."""
        server = FixtureHTTPServer(fixtures_dir=str(sample_fixture))
        
        with pytest.raises(RuntimeError):
            server.get_rewritten_url("https://example.com/page")
    
    def test_pytest_fixture_works(self, mock_http_server):
        """mock_http_server pytest fixture yields working server."""
        # Create a test fixture
        fixtures_dir = Path(mock_http_server.fixtures_dir)
        doc_dir = fixtures_dir / "pytest-doc"
        doc_dir.mkdir()
        
        meta = {
            "status": 200,
            "headers": {},
            "original_url": "https://pytest.org/page",
            "slug": "index"
        }
        with open(doc_dir / "index.meta.json", 'w') as f:
            json.dump(meta, f)
        with open(doc_dir / "index.body.html", 'w') as f:
            f.write("<html>PyTest</html>")
        
        # Server should respond
        response = requests.get(f"{mock_http_server.base_url}/pytest-doc/index")
        assert response.status_code == 200
        assert "PyTest" in response.text


class TestURLRewriting:
    """Tests for URL rewriting logic."""
    
    @pytest.fixture
    def server(self, tmp_path):
        """Server fixture for URL tests."""
        server = FixtureHTTPServer(fixtures_dir=str(tmp_path / "fixtures"))
        server.start()
        yield server
        server.stop()
    
    def test_rewrites_https_to_localhost(self, server):
        """HTTPS URLs are rewritten to localhost."""
        rewritten = server.get_rewritten_url("https://example.com/path")
        assert rewritten.startswith("http://localhost:")
    
    def test_rewrites_http_to_localhost(self, server):
        """HTTP URLs are also rewritten."""
        rewritten = server.get_rewritten_url("http://example.com/path")
        assert rewritten.startswith("http://localhost:")
    
    def test_converts_domain_to_slug(self, server):
        """Domain first part is used as doc name."""
        rewritten = server.get_rewritten_url("https://react.dev/learn")
        assert "/react/" in rewritten
    
    def test_converts_path_to_slug(self, server):
        """Path is converted to slug format."""
        rewritten = server.get_rewritten_url("https://example.com/some/deep/path")
        assert "some-deep-path" in rewritten
    
    def test_handles_root_path(self, server):
        """Root paths become 'index'."""
        rewritten = server.get_rewritten_url("https://example.com/")
        assert rewritten.endswith("/example/index")


class TestServerLifecycle:
    """Tests for server start/stop behavior."""
    
    def test_stop_shuts_down_server(self, tmp_path):
        """stop() properly shuts down the server."""
        fixtures_dir = tmp_path / "fixtures"
        server = FixtureHTTPServer(fixtures_dir=str(fixtures_dir))
        base_url = server.start()
        
        # Verify server works
        response = requests.get(base_url)
        # 404 is expected since no fixtures, but server responds
        
        # Stop server
        server.stop()
        
        # Server should no longer respond
        with pytest.raises(requests.ConnectionError):
            requests.get(base_url, timeout=1)
