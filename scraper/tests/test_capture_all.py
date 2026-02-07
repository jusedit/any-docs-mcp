"""Tests for capture_all runner script."""
import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch

capture_all = pytest.importorskip("capture_all")


class TestManifestValidation:
    """Tests for capture-manifest.json validation."""
    
    @pytest.fixture
    def manifest(self):
        """Load the real capture manifest."""
        # Path relative to project root
        manifest_path = Path(__file__).parent.parent.parent / "tests" / "fixtures" / "real-world" / "capture-manifest.json"
        with open(manifest_path) as f:
            return json.load(f)
    
    def test_manifest_has_version(self, manifest):
        """Manifest has version field."""
        assert "version" in manifest
    
    def test_manifest_has_doc_sets(self, manifest):
        """Manifest has exactly 10 doc-sets."""
        assert "doc_sets" in manifest
        assert len(manifest["doc_sets"]) == 10
    
    def test_each_doc_set_has_required_fields(self, manifest):
        """Each doc-set has doc_name, site_type, base_url, urls."""
        required = ["doc_name", "site_type", "base_url", "urls"]
        for doc_set in manifest["doc_sets"]:
            for field in required:
                assert field in doc_set, f"{doc_set.get('doc_name', 'unknown')} missing {field}"
    
    def test_each_url_has_required_fields(self, manifest):
        """Each URL entry has url and page_type."""
        for doc_set in manifest["doc_sets"]:
            for url_entry in doc_set["urls"]:
                assert "url" in url_entry
                assert "page_type" in url_entry
    
    def test_doc_sets_are_expected_ones(self, manifest):
        """Doc-sets match the expected 10 reference sets."""
        expected = {
            "react", "fastapi", "tailwind", "kubernetes", "django",
            "hyperapp-github", "onoffice", "synthflow", "golang", "rust-book"
        }
        actual = {ds["doc_name"] for ds in manifest["doc_sets"]}
        assert actual == expected
    
    def test_each_doc_set_has_3_to_5_urls(self, manifest):
        """Each doc-set has 3-5 URLs."""
        for doc_set in manifest["doc_sets"]:
            url_count = len(doc_set["urls"])
            # GitHub raw sources may have fewer URLs
            if doc_set["site_type"] == "github":
                assert url_count >= 1, f"{doc_set['doc_name']} has {url_count} URLs (expected at least 1)"
            else:
                assert 3 <= url_count <= 5, f"{doc_set['doc_name']} has {url_count} URLs (expected 3-5)"
    
    def test_hyperapp_github_has_fewer_urls(self, manifest):
        """GitHub raw sources may have fewer URLs."""
        hyperapp = next(ds for ds in manifest["doc_sets"] if ds["doc_name"] == "hyperapp-github")
        assert len(hyperapp["urls"]) >= 1  # May have just 1
    
    def test_page_types_are_valid(self, manifest):
        """Page types are from allowed set."""
        valid_types = {"landing", "tutorial", "api_reference", "code_examples", "edge_case"}
        for doc_set in manifest["doc_sets"]:
            for url_entry in doc_set["urls"]:
                assert url_entry["page_type"] in valid_types


class TestCaptureAll:
    """Tests for capture_all() function."""
    
    @pytest.fixture
    def mock_manifest(self, tmp_path):
        """Create a minimal mock manifest."""
        manifest = {
            "version": "1.0.0",
            "doc_sets": [
                {
                    "doc_name": "test-doc",
                    "site_type": "custom",
                    "base_url": "https://example.com",
                    "urls": [
                        {"url": "https://example.com/page1", "page_type": "landing"},
                        {"url": "https://example.com/page2", "page_type": "tutorial"}
                    ]
                }
            ]
        }
        manifest_path = tmp_path / "test-manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f)
        return str(manifest_path)
    
    @pytest.fixture
    def mock_capture(self):
        """Create a mock ResponseCapture."""
        mock_resp = Mock()
        mock_resp.status = 200
        mock_resp.headers = {}
        mock_resp.body = "<html>Test</html>"
        mock_resp.url = "https://example.com/page"
        mock_resp.captured_at = "2024-01-01T00:00:00Z"
        
        mock_capture = Mock()
        mock_capture.capture.return_value = mock_resp
        mock_capture.save.return_value = (Mock(), Mock())
        return mock_capture
    
    def test_capture_all_returns_report(self, mock_manifest, tmp_path):
        """capture_all() returns a report dict."""
        with patch('capture_all.ResponseCapture') as MockCapture:
            mock_capture = Mock()
            mock_capture.capture.return_value = Mock()
            mock_capture.save.return_value = (Mock(), Mock())
            MockCapture.return_value = mock_capture
            
            results = capture_all.capture_all(
                manifest_path=mock_manifest,
                fixtures_dir=str(tmp_path / "fixtures")
            )
        
        assert isinstance(results, dict)
        assert "captured_count" in results
        assert "errors" in results
        assert "total_urls" in results
    
    def test_capture_all_counts_total_urls(self, mock_manifest, tmp_path):
        """Report includes correct total URL count."""
        with patch('capture_all.ResponseCapture') as MockCapture:
            mock_capture = Mock()
            mock_capture.capture.return_value = Mock()
            mock_capture.save.return_value = (Mock(), Mock())
            MockCapture.return_value = mock_capture
            
            results = capture_all.capture_all(manifest_path=mock_manifest)
        
        assert results["total_urls"] == 2  # 2 URLs in mock manifest
    
    def test_capture_all_respects_doc_set_filter(self, mock_manifest, tmp_path):
        """doc_sets parameter filters which doc-sets to capture."""
        with patch('capture_all.ResponseCapture') as MockCapture:
            mock_capture = Mock()
            mock_capture.capture.return_value = Mock()
            mock_capture.save.return_value = (Mock(), Mock())
            MockCapture.return_value = mock_capture
            
            # Filter to non-existent doc-set
            results = capture_all.capture_all(
                doc_sets=["non-existent"],
                manifest_path=mock_manifest
            )
        
        assert results["captured_count"] == 0
        assert results["total_urls"] == 0  # No matching doc-sets
    
    def test_capture_all_records_errors(self, mock_manifest, tmp_path):
        """Errors are recorded in the report."""
        with patch('capture_all.ResponseCapture') as MockCapture:
            mock_capture = Mock()
            mock_capture.capture.side_effect = Exception("Network error")
            MockCapture.return_value = mock_capture
            
            results = capture_all.capture_all(manifest_path=mock_manifest)
        
        assert len(results["errors"]) == 2  # Both URLs failed
        assert results["captured_count"] == 0


class TestCLI:
    """Tests for CLI functionality."""
    
    def test_list_flag_shows_doc_sets(self, capsys):
        """--list flag outputs doc-set information."""
        manifest_path = Path(__file__).parent.parent.parent / "tests" / "fixtures" / "real-world" / "capture-manifest.json"
        
        with pytest.raises(SystemExit) as exc_info:
            with patch('sys.argv', ['capture_all.py', '--list', '--manifest', str(manifest_path)]):
                capture_all.main()
        
        # Should exit successfully
        assert exc_info.value.code == 0
        
        captured = capsys.readouterr()
        # Should show doc-set names
        assert "react" in captured.out or "fastapi" in captured.out
    
    def test_list_shows_url_counts(self, capsys):
        """--list shows URL counts per doc-set."""
        manifest_path = Path(__file__).parent.parent.parent / "tests" / "fixtures" / "real-world" / "capture-manifest.json"
        
        with pytest.raises(SystemExit):
            with patch('sys.argv', ['capture_all.py', '--list', '--manifest', str(manifest_path)]):
                capture_all.main()
        
        captured = capsys.readouterr()
        # Should show "X URLs" pattern
        assert "URLs" in captured.out


class TestLoadManifest:
    """Tests for load_manifest() function."""
    
    def test_loads_real_manifest(self):
        """Can load the actual capture-manifest.json."""
        # Use absolute path from project root
        manifest_path = Path(__file__).parent.parent.parent / "tests" / "fixtures" / "real-world" / "capture-manifest.json"
        manifest = capture_all.load_manifest(str(manifest_path))
        
        assert "doc_sets" in manifest
        assert len(manifest["doc_sets"]) == 10
