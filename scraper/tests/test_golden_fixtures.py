"""Tests for golden fixture files and quality baseline."""
import pytest
import json
from pathlib import Path


class TestGoldenFixturesExist:
    """Tests validating golden fixture files exist."""
    
    @pytest.fixture(scope="module")
    def fixtures_dir(self):
        """Return path to real-world fixtures directory."""
        return Path(__file__).parent.parent.parent / "tests" / "fixtures" / "real-world"
    
    def test_react_golden_exists(self, fixtures_dir):
        """React golden directory has .md files."""
        golden_dir = fixtures_dir / "react" / "golden"
        assert golden_dir.exists()
        md_files = list(golden_dir.glob("*.md"))
        assert len(md_files) >= 1
    
    def test_fastapi_golden_exists(self, fixtures_dir):
        """FastAPI golden directory has .md files."""
        golden_dir = fixtures_dir / "fastapi" / "golden"
        assert golden_dir.exists()
        md_files = list(golden_dir.glob("*.md"))
        assert len(md_files) >= 1
    
    def test_tailwind_golden_exists(self, fixtures_dir):
        """Tailwind golden directory has .md files."""
        golden_dir = fixtures_dir / "tailwind" / "golden"
        assert golden_dir.exists()
        md_files = list(golden_dir.glob("*.md"))
        assert len(md_files) >= 1
    
    def test_golden_files_are_not_stubs(self, fixtures_dir):
        """Golden files are content-rich (>500 chars)."""
        for golden_dir in fixtures_dir.glob("*/golden"):
            for md_file in golden_dir.glob("*.md"):
                content = md_file.read_text(encoding='utf-8')
                assert len(content) > 500, f"{md_file} is too short ({len(content)} chars)"
    
    def test_golden_files_have_headings(self, fixtures_dir):
        """Golden files have markdown headings."""
        import re
        for golden_dir in fixtures_dir.glob("*/golden"):
            for md_file in golden_dir.glob("*.md"):
                content = md_file.read_text(encoding='utf-8')
                headings = re.findall(r'^#{1,6}\s', content, re.MULTILINE)
                assert len(headings) > 0, f"{md_file} has no headings"


class TestQualityBaseline:
    """Tests for quality_baseline.json."""
    
    @pytest.fixture(scope="module")
    def baseline(self):
        """Load quality baseline JSON."""
        baseline_path = Path(__file__).parent.parent.parent / "tests" / "fixtures" / "real-world" / "quality_baseline.json"
        with open(baseline_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_baseline_has_version(self, baseline):
        """Baseline has version field."""
        assert "version" in baseline
    
    def test_baseline_has_files(self, baseline):
        """Baseline has files dict."""
        assert "files" in baseline
        assert len(baseline["files"]) > 0
    
    def test_baseline_has_summary(self, baseline):
        """Baseline has summary section."""
        assert "summary" in baseline
        summary = baseline["summary"]
        assert "total_files" in summary
        assert "total_chars" in summary
        assert "total_headings" in summary
        assert "total_code_blocks" in summary
        assert "total_encoding_errors" in summary
        assert "total_artifacts" in summary
    
    def test_each_file_has_required_metrics(self, baseline):
        """Each file entry has all required metrics."""
        required = ["char_count", "line_count", "heading_count", 
                    "code_block_count", "encoding_errors", "artifacts"]
        for file_key, metrics in baseline["files"].items():
            for field in required:
                assert field in metrics, f"{file_key} missing {field}"
    
    def test_file_count_matches_summary(self, baseline):
        """Summary total_files matches files dict length."""
        assert baseline["summary"]["total_files"] == len(baseline["files"])


class TestGenerateBaselineScript:
    """Tests for generate_baseline.py script."""
    
    def test_script_exists(self):
        """generate_baseline.py script exists."""
        script_path = Path(__file__).parent.parent / "generate_baseline.py"
        assert script_path.exists()
    
    def test_script_runs_without_error(self, tmp_path):
        """Script executes without error on temp fixtures."""
        import subprocess
        import sys
        
        script_path = Path(__file__).parent.parent / "generate_baseline.py"
        
        # Create temp fixtures dir
        fixtures_dir = tmp_path / "fixtures"
        golden_dir = fixtures_dir / "test-doc" / "golden"
        golden_dir.mkdir(parents=True)
        
        # Create a test markdown file
        (golden_dir / "test.md").write_text("# Test\n\nSome content\n\n```python\nprint('hello')\n```")
        
        output_path = tmp_path / "baseline.json"
        
        # Run script
        result = subprocess.run(
            [sys.executable, str(script_path), 
             "--fixtures-dir", str(fixtures_dir),
             "--output", str(output_path)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        assert output_path.exists()
        
        # Verify output is valid JSON
        with open(output_path) as f:
            baseline = json.load(f)
        assert baseline["summary"]["total_files"] == 1
