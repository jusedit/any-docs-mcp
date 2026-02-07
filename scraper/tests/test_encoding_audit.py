"""Tests for encoding audit script."""
import pytest
import json
from pathlib import Path

from encoding_audit import EncodingAuditor, Defect, AuditReport, format_report


class TestScanText:
    """Tests for scan_text() method with inline strings."""
    
    def test_detects_mojibake_curly_quotes(self):
        """Detects mojibake curly quotes."""
        auditor = EncodingAuditor()
        text = "This has â€™ and â€œ characters"
        defects = auditor.scan_text(text)
        
        assert len(defects) == 2
        assert all(d.category == "mojibake" for d in defects)
    
    def test_detects_broken_latin_supplement(self):
        """Detects orphan Latin-1 supplement characters."""
        auditor = EncodingAuditor()
        # Use raw bytes that decode to Â + control char pattern
        text = "Heading with \xc2\x80 character"  # Â€ in UTF-8
        defects = auditor.scan_text(text)
        
        # Should find broken_latin pattern
        assert any(d.category == "broken_latin" for d in defects)
    
    def test_detects_permalink_anchors(self):
        """Detects Â¶ permalink anchor characters."""
        auditor = EncodingAuditor()
        text = "## SecurityÂ¶"
        defects = auditor.scan_text(text)
        
        # Â¶ matches both broken_latin and permalink_anchors
        assert len(defects) == 2
        assert any(d.category == "permalink_anchors" for d in defects)
    
    def test_detects_permalink_links(self):
        """Detects [¶](#anchor) permalink links."""
        auditor = EncodingAuditor()
        text = '## OAuth2[¶](#oauth2 "link")'
        defects = auditor.scan_text(text)
        
        assert len(defects) == 1
        assert "permalink" in defects[0].category
    
    def test_detects_html_entities(self):
        """Detects HTML entities like &amp; &lt;."""
        auditor = EncodingAuditor()
        text = "Use &amp; for AND and &lt; for less than"
        defects = auditor.scan_text(text)
        
        assert len(defects) == 2
        assert all(d.category == "html_entities" for d in defects)
    
    def test_includes_context_in_defect(self):
        """Defect includes context around match."""
        auditor = EncodingAuditor()
        text = "Some text before â€™ and after"
        defects = auditor.scan_text(text)
        
        assert len(defects) == 1
        assert "before" in defects[0].context
        assert "after" in defects[0].context
    
    def test_includes_line_number(self):
        """Defect includes correct line number."""
        auditor = EncodingAuditor()
        # â€™ matches mojibake pattern on second line
        text = "Line 1\nLine 2 with â€™\nLine 3"
        defects = auditor.scan_text(text)
        
        mojibake_defects = [d for d in defects if d.category == "mojibake"]
        assert len(mojibake_defects) == 1
        assert mojibake_defects[0].line_number == 2


class TestScanFile:
    """Tests for scan_file() method."""
    
    def test_scans_single_file(self, tmp_path):
        """scan_file() finds defects in a file."""
        file_path = tmp_path / "test.md"
        file_path.write_text("## HeadingÂ¶\n\nSome â€™ content", encoding='utf-8')
        
        auditor = EncodingAuditor()
        defects = auditor.scan_file(file_path)
        
        # Â¶ matches both broken_latin and permalink_anchors patterns
        assert len(defects) == 3  # 2 from Â¶ + 1 from â€™
        assert any(d.category == "permalink_anchors" for d in defects)
        assert any(d.category == "mojibake" for d in defects)
        assert any(d.category == "broken_latin" for d in defects)
    
    def test_returns_file_path_in_defects(self, tmp_path):
        """Defects include the file path."""
        file_path = tmp_path / "test.md"
        file_path.write_text("Â¶", encoding='utf-8')
        
        auditor = EncodingAuditor()
        defects = auditor.scan_file(file_path)
        
        # Â¶ matches both patterns
        assert len(defects) == 2
        assert str(file_path) in defects[0].file_path


class TestScanDirectory:
    """Tests for scan_directory() method."""
    
    @pytest.fixture
    def fixture_dir(self, tmp_path):
        """Create directory with test markdown files."""
        # File with mojibake
        (tmp_path / "file1.md").write_text("Text with â€™ quote", encoding='utf-8')
        
        # File with permalink
        (tmp_path / "file2.md").write_text("## HeadingÂ¶", encoding='utf-8')
        
        # Clean file
        (tmp_path / "file3.md").write_text("# Clean\n\nNo defects here.", encoding='utf-8')
        
        return tmp_path
    
    def test_returns_audit_report(self, fixture_dir):
        """scan_directory() returns AuditReport."""
        auditor = EncodingAuditor()
        report = auditor.scan_directory(str(fixture_dir))
        
        assert isinstance(report, AuditReport)
        assert report.total_files == 3
    
    def test_counts_affected_files(self, fixture_dir):
        """Report correctly counts affected files."""
        auditor = EncodingAuditor()
        report = auditor.scan_directory(str(fixture_dir))
        
        # 2 files have defects, 1 is clean
        assert report.affected_files == 2
    
    def test_defects_by_category(self, fixture_dir):
        """Report categorizes defects correctly."""
        auditor = EncodingAuditor()
        report = auditor.scan_directory(str(fixture_dir))
        
        assert "mojibake" in report.defects_by_category
        assert "permalink_anchors" in report.defects_by_category
        assert report.defects_by_category["mojibake"] == 1
        assert report.defects_by_category["permalink_anchors"] == 1
    
    def test_collects_all_defects(self, fixture_dir):
        """Report includes all found defects."""
        auditor = EncodingAuditor()
        report = auditor.scan_directory(str(fixture_dir))
        
        # 1 mojibake + 2 from Â¶ (broken_latin + permalink)
        assert len(report.defects) == 3


class TestFormatReport:
    """Tests for format_report() function."""
    
    def test_format_returns_dict(self):
        """format_report() returns JSON-serializable dict."""
        report = AuditReport(
            total_files=5,
            affected_files=3,
            defects_by_category={"mojibake": 2, "permalink": 1},
            defects=[
                Defect("mojibake", "â€™", "file.md", 1, "context"),
                Defect("permalink", "Â¶", "file.md", 2, "context")
            ]
        )
        
        formatted = format_report(report)
        
        assert isinstance(formatted, dict)
        assert formatted["total_files"] == 5
        assert formatted["affected_files"] == 3
        assert formatted["defects_by_category"]["mojibake"] == 2
        assert len(formatted["defects"]) == 2


class TestCLI:
    """Tests for CLI functionality."""
    
    def test_script_has_main(self):
        """encoding_audit.py has main() function."""
        import encoding_audit as ea
        assert hasattr(ea, 'main')
    
    def test_cli_runs_without_error(self, tmp_path):
        """CLI runs without error on temp directory."""
        import subprocess
        import sys
        
        # Create test file
        (tmp_path / "test.md").write_text("Â¶", encoding='utf-8')
        
        script_path = Path(__file__).parent.parent / "encoding_audit.py"
        result = subprocess.run(
            [sys.executable, str(script_path), str(tmp_path), "--summary"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "Files scanned" in result.stdout
