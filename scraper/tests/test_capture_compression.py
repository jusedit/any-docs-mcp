"""Tests for capture compression and storage optimization."""
import gzip
import pytest
import sys
import tempfile
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))

from response_capture import ResponseCapture, CapturedResponse


class TestCaptureCompression:
    """Test gzip compression for large captured files."""
    
    def test_compresses_files_over_threshold(self):
        """Files >100KB are automatically gzip compressed."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            capture = ResponseCapture(fixtures_dir=tmp_dir)
            
            # Create a large response (>100KB)
            large_body = "A" * 150000
            resp = CapturedResponse(
                status=200,
                headers={"Content-Type": "text/html"},
                body=large_body,
                url="https://example.com/large-page"
            )
            
            meta_path, body_path = capture.save(resp, "test-doc", compress_threshold_kb=100)
            
            # Should have .gz extension
            assert body_path.suffix == ".gz"
            assert body_path.name.endswith(".body.html.gz")
            
            # Should be smaller than original
            original_size = len(large_body.encode('utf-8'))
            compressed_size = body_path.stat().st_size
            assert compressed_size < original_size * 0.5  # At least 50% compression
            
            # Meta should have compression info
            import json
            meta = json.loads(meta_path.read_text())
            assert meta["compression"]["enabled"] is True
            assert meta["compression"]["original_size_bytes"] == original_size
            assert meta["compression"]["savings_percent"] > 0
    
    def test_small_files_not_compressed(self):
        """Files <100KB are not compressed."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            capture = ResponseCapture(fixtures_dir=tmp_dir)
            
            # Create a small response (<100KB)
            small_body = "<html><body>Test</body></html>"
            resp = CapturedResponse(
                status=200,
                headers={"Content-Type": "text/html"},
                body=small_body,
                url="https://example.com/small-page"
            )
            
            meta_path, body_path = capture.save(resp, "test-doc", compress_threshold_kb=100)
            
            # Should NOT have .gz extension
            assert not body_path.name.endswith(".gz")
            assert body_path.name.endswith(".body.html")
            
            # Meta should show no compression
            import json
            meta = json.loads(meta_path.read_text())
            assert meta["compression"]["enabled"] is False
            assert meta["compression"]["savings_percent"] == 0
    
    def test_load_handles_both_compressed_and_uncompressed(self):
        """load() method handles both .html and .html.gz files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            capture = ResponseCapture(fixtures_dir=tmp_dir)
            
            # Save uncompressed
            small_resp = CapturedResponse(
                status=200,
                headers={},
                body="Small content",
                url="https://example.com/small"
            )
            meta1, body1 = capture.save(small_resp, "test", compress_threshold_kb=1000)
            
            # Save compressed (force by using very low threshold)
            large_resp = CapturedResponse(
                status=200,
                headers={},
                body="Large content: " + "A" * 2000,
                url="https://example.com/large"
            )
            meta2, body2 = capture.save(large_resp, "test", compress_threshold_kb=1)
            
            # Load both
            slug1 = body1.stem.replace('.body', '')
            slug2 = body2.stem.replace('.body', '').replace('.html', '')  # Handle .gz
            
            loaded1 = capture.load("test", slug1)
            loaded2 = capture.load("test", slug2)
            
            assert loaded1.body == "Small content"
            assert "Large content" in loaded2.body


class TestFixtureServerWithCompression:
    """Test FixtureHTTPServer serves .gz files transparently."""
    
    def test_server_serves_compressed_files(self):
        """Server decompresses and serves .gz files."""
        from tests.fixture_server import FixtureHTTPServer
        import requests
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create a compressed fixture
            doc_dir = Path(tmp_dir) / "test-site"
            doc_dir.mkdir()
            
            # Write meta
            meta = {
                "status": 200,
                "headers": {"Content-Type": "text/html"},
                "original_url": "https://example.com/page",
                "slug": "test-page",
                "compression": {"enabled": True}
            }
            import json
            (doc_dir / "test-page.meta.json").write_text(json.dumps(meta))
            
            # Write compressed body
            body = "<html><body>Compressed content</body></html>"
            compressed = gzip.compress(body.encode('utf-8'))
            (doc_dir / "test-page.body.html.gz").write_bytes(compressed)
            
            # Start server
            server = FixtureHTTPServer(tmp_dir)
            base_url = server.start()
            
            try:
                response = requests.get(f"{base_url}/test-site/test-page", timeout=5)
                assert response.status_code == 200
                assert "Compressed content" in response.text
            finally:
                server.stop()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
