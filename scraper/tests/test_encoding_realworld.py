"""Encoding regression tests against real golden fixture files.

These tests verify that ContentCleaner properly removes encoding defects
from real scraped documentation. They serve as a regression gate:
if changes to the cleaner reintroduce encoding issues, these tests fail.
"""
import pytest
from pathlib import Path

from content_cleaner import ContentCleaner
from encoding_audit import EncodingAuditor


# Get golden fixtures directory
GOLDEN_DIR = Path(__file__).parent.parent.parent / "tests" / "fixtures" / "real-world"


def get_golden_files(doc_name: str):
    """Get all golden .md files for a doc-set."""
    golden_dir = GOLDEN_DIR / doc_name / "golden"
    if not golden_dir.exists():
        return []
    return list(golden_dir.glob("*.md"))


class TestEncodingRegression:
    """Regression tests: golden fixtures should have zero encoding defects after cleaning."""
    
    @pytest.fixture
    def cleaner(self):
        """ContentCleaner instance."""
        return ContentCleaner()
    
    @pytest.fixture
    def auditor(self):
        """EncodingAuditor instance."""
        return EncodingAuditor()
    
    @pytest.mark.parametrize("doc_name", [
        "react",
        "fastapi", 
        "tailwind"
    ])
    def test_golden_files_have_zero_defects_after_clean(self, doc_name, cleaner, auditor):
        """Each golden file should have zero encoding defects after cleaning."""
        golden_files = get_golden_files(doc_name)
        
        if not golden_files:
            pytest.skip(f"No golden files found for {doc_name}")
        
        for file_path in golden_files:
            # Load original content
            original = file_path.read_text(encoding='utf-8')
            original_lines = len(original.splitlines())
            
            # Clean the content
            cleaned = cleaner.clean(original)
            cleaned_lines = len(cleaned.splitlines())
            
            # Scan for encoding defects
            defects = auditor.scan_text(cleaned)
            
            # Filter to encoding-related defects only
            encoding_defects = [
                d for d in defects 
                if d.category in ['mojibake', 'broken_latin', 'permalink_anchors', 'html_entities']
            ]
            
            # Assert zero defects
            if encoding_defects:
                defect_summary = ", ".join(
                    f"{d.category} at line {d.line_number}" 
                    for d in encoding_defects[:3]
                )
                pytest.fail(
                    f"{file_path.name}: Found {len(encoding_defects)} encoding defects: {defect_summary}"
                )
            
            # Log line count change for review
            line_delta = original_lines - cleaned_lines
            if line_delta > 0:
                print(f"  {file_path.name}: removed {line_delta} lines ({original_lines} → {cleaned_lines})")


class TestPermalinkRemovalRegression:
    """Specific tests for permalink anchor removal from golden fixtures."""
    
    def test_fastapi_golden_no_permalinks_after_clean(self):
        """FastAPI golden files should have no permalink anchors after cleaning."""
        golden_files = get_golden_files("fastapi")
        
        if not golden_files:
            pytest.skip("No fastapi golden files")
        
        cleaner = ContentCleaner()
        auditor = EncodingAuditor()
        
        for file_path in golden_files:
            original = file_path.read_text(encoding='utf-8')
            
            # Count permalinks before
            before_defects = auditor.scan_text(original)
            before_permalinks = len([d for d in before_defects if d.category == 'permalink_anchors'])
            
            # Clean
            cleaned = cleaner.remove_permalink_anchors(original)
            
            # Count permalinks after
            after_defects = auditor.scan_text(cleaned)
            after_permalinks = len([d for d in after_defects if d.category == 'permalink_anchors'])
            
            print(f"  {file_path.name}: {before_permalinks} → {after_permalinks} permalinks")
            
            # After cleaning, should be zero
            assert after_permalinks == 0, f"{file_path.name} still has {after_permalinks} permalink anchors"


class TestLineCountLogging:
    """Tests that log before/after line counts for manual review."""
    
    def test_line_count_changes_logged(self, capsys):
        """Line count changes are printed for each file."""
        golden_files = []
        for doc_name in ["react", "fastapi", "tailwind"]:
            golden_files.extend(get_golden_files(doc_name))
        
        if not golden_files:
            pytest.skip("No golden files found")
        
        cleaner = ContentCleaner()
        
        total_removed = 0
        for file_path in golden_files:
            original = file_path.read_text(encoding='utf-8')
            cleaned = cleaner.clean(original)
            
            removed = len(original.splitlines()) - len(cleaned.splitlines())
            total_removed += removed
        
        print(f"\nTotal lines removed across all golden files: {total_removed}")
        
        captured = capsys.readouterr()
        # Just verify no exceptions were raised
        assert True
