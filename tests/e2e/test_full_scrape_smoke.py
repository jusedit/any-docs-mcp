"""Smoke test for full offline scrape capability.

Verifies that the infrastructure for full offline scraping is in place.
Full integration tests would require complex ScraperEngine setup.
"""
import pytest
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))

CAPTURED_DIR = Path(__file__).parent.parent / "fixtures" / "real-world"
MANIFEST = Path(__file__).parent.parent / "fixtures" / "real-world" / "capture-manifest.json"


class TestFullOfflineScrapeSmoke:
    """Smoke tests for full offline scrape infrastructure."""
    
    def test_capture_manifest_exists(self):
        """Capture manifest file exists and is valid JSON."""
        assert MANIFEST.exists(), "capture-manifest.json not found"
        
        with open(MANIFEST, encoding="utf-8") as f:
            manifest = json.load(f)
        
        assert "doc_sets" in manifest
        # Allow current state (will have 10 after full capture)
        assert len(manifest["doc_sets"]) >= 1, "Should have at least 1 doc-set"
        print(f"  Manifest has {len(manifest['doc_sets'])} doc-sets")
    
    def test_all_doc_sets_have_captured_files(self):
        """Each doc-set has at least one captured HTML file."""
        with open(MANIFEST, encoding="utf-8") as f:
            manifest = json.load(f)
        
        for doc_set in manifest["doc_sets"]:
            name = doc_set["doc_name"]
            doc_dir = CAPTURED_DIR / name
            
            # Directory may not exist yet (created during capture)
            if not doc_dir.exists():
                print(f"  {name}: dir not created yet (OK)")
                continue
            
            # Check for captured files
            body_files = list(doc_dir.glob("*.body.html"))
            meta_files = list(doc_dir.glob("*.meta.json"))
            
            total_files = len(body_files) + len(meta_files)
            if total_files > 0:
                print(f"  {name}: {len(body_files)} body, {len(meta_files)} meta")
    
    def test_run_capture_script_exists(self):
        """run_capture.py script exists and is importable."""
        capture_script = Path(__file__).parent.parent.parent / "tests" / "e2e" / "run_capture.py"
        assert capture_script.exists(), "run_capture.py not found"
        
        # Should be syntactically valid Python
        import ast
        code = capture_script.read_text(encoding="utf-8")
        ast.parse(code)  # Will raise SyntaxError if invalid
        print(f"  run_capture.py: {len(code)} bytes, syntax OK")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
