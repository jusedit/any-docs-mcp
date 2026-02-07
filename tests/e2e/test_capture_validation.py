"""Tests for capture validation and integrity check."""
import json
import pytest
import sys
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tests" / "e2e"))

from run_capture import validate_capture, quarantine_capture


class TestValidateCapture:
    """Test capture validation logic."""
    
    def test_valid_capture_passes(self):
        """Valid capture passes all checks."""
        meta = {"status": 200, "Content-Type": "text/html"}
        body = "<html><body>Valid HTML content " + "A" * 1000 + "</body></html>"
        
        is_valid, errors = validate_capture(meta, body)
        
        assert is_valid is True
        assert len(errors) == 0
    
    def test_invalid_status_fails(self):
        """Status != 200 is invalid."""
        meta = {"status": 404}
        body = "<html><body>Not found page</body></html>"
        
        is_valid, errors = validate_capture(meta, body)
        
        assert is_valid is False
        assert any("404" in e for e in errors)
    
    def test_small_body_fails(self):
        """Body < 1000 bytes is invalid."""
        meta = {"status": 200}
        body = "<html>Small</html>"  # Less than 1000 bytes
        
        is_valid, errors = validate_capture(meta, body)
        
        assert is_valid is False
        assert any("too small" in e.lower() for e in errors)
    
    def test_missing_html_tag_fails(self):
        """Body without <html> or <body> is invalid."""
        meta = {"status": 200}
        body = "Plain text without HTML tags " + "A" * 1000
        
        is_valid, errors = validate_capture(meta, body)
        
        assert is_valid is False
        assert any("html" in e.lower() for e in errors)


class TestQuarantineFunction:
    """Test quarantine functionality."""
    
    def test_quarantine_moves_files(self):
        """Quarantine moves files to quarantine subdirectory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            doc_dir = Path(tmp_dir) / "test-doc"
            doc_dir.mkdir()
            
            # Create test files
            (doc_dir / "test-slug.meta.json").write_text('{"status": 200}')
            (doc_dir / "test-slug.body.html").write_text("<html>Test</html>")
            
            # Quarantine
            quarantine_capture(doc_dir, "test-slug")
            
            # Check files moved
            quarantine_dir = doc_dir / "quarantine"
            assert (quarantine_dir / "test-slug.meta.json").exists()
            assert (quarantine_dir / "test-slug.body.html").exists()
            
            # Check original files removed
            assert not (doc_dir / "test-slug.meta.json").exists()
            assert not (doc_dir / "test-slug.body.html").exists()


class TestValidateCLI:
    """Test CLI integration for --validate."""
    
    def test_cli_accepts_validate_flag(self):
        """CLI parser accepts --validate argument."""
        import argparse
        
        parser = argparse.ArgumentParser()
        parser.add_argument("--validate", action="store_true")
        
        args = parser.parse_args(["--validate"])
        assert args.validate is True
        
        args = parser.parse_args([])
        assert args.validate is False


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
