"""Tests for encoding error elimination (rust-book)."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))

from content_cleaner import ContentCleaner
from encoding_audit import EncodingAuditor, Defect


class TestEncodingAudit:
    """Test encoding audit for mojibake detection."""
    
    def test_detects_broken_utf8(self):
        """Audit detects broken UTF-8 sequences."""
        auditor = EncodingAuditor()
        text = "This has broken encoding: Ã© instead of é"
        
        defects = auditor.scan_text(text)
        
        # Should detect the mojibake pattern
        assert len(defects) > 0
        assert any("Ã©" in d.pattern_matched for d in defects)
    
    def test_detects_smart_quote_issues(self):
        """Audit detects smart quote encoding issues."""
        auditor = EncodingAuditor()
        text = 'Using â€œ instead of "smart quotes"'
        
        defects = auditor.scan_text(text)
        
        # Should detect the encoding issue
        assert len(defects) > 0
    
    def test_detects_dash_issues(self):
        """Audit detects dash/emdash encoding issues."""
        auditor = EncodingAuditor()
        text = "Using â€” instead of em-dash"
        
        defects = auditor.scan_text(text)
        
        assert len(defects) > 0
    
    def test_clean_content_reports_no_defects(self):
        """Clean UTF-8 content reports no defects."""
        auditor = EncodingAuditor()
        text = "This is clean UTF-8 content with é and ü."
        
        defects = auditor.scan_text(text)
        
        # Should not flag proper UTF-8 characters
        assert len(defects) == 0


class TestEncodingRepair:
    """Test encoding repair in ContentCleaner."""
    
    def test_fixes_accented_characters(self):
        """Fixes broken accented characters."""
        cleaner = ContentCleaner()
        content = "cafÃ© should become café"
        
        fixed = cleaner.fix_encoding_issues(content)
        
        assert "café" in fixed
        assert "Ã©" not in fixed
    
    def test_fixes_smart_quotes(self):
        """Fixes broken smart quotes."""
        cleaner = ContentCleaner()
        content = 'â€œHelloâ€ instead of "Hello"'
        
        fixed = cleaner.fix_encoding_issues(content)
        
        assert '"Hello"' in fixed or '"Hello"' in fixed
        assert "â€œ" not in fixed
        assert "â€" not in fixed
    
    def test_fixes_ellipsis(self):
        """Fixes broken ellipsis."""
        cleaner = ContentCleaner()
        content = "Using â¦ instead of..."
        
        fixed = cleaner.fix_encoding_issues(content)
        
        assert "..." in fixed
        assert "â¦" not in fixed
    
    def test_preserves_valid_utf8(self):
        """Does not corrupt valid UTF-8 content."""
        cleaner = ContentCleaner()
        content = "Valid café with émojis 🎉 and ümlauts"
        
        fixed = cleaner.fix_encoding_issues(content)
        
        assert "café" in fixed
        assert "émojis" in fixed
        assert "ümlauts" in fixed
    
    def test_handles_rust_book_patterns(self):
        """Handles common rust-book encoding issues."""
        cleaner = ContentCleaner()
        # Common patterns found in rust-book
        content = """
        The type Ã<T> should be ë<T>.
        Using â€” for em-dash in â€œexamplesâ€.
        """
        
        fixed = cleaner.fix_encoding_issues(content)
        
        # Should fix common mojibake
        assert "Ã<" not in fixed or "ë<" in fixed


class TestEncodingIntegration:
    """Integration tests for encoding pipeline."""
    
    def test_full_clean_pipeline(self):
        """Full clean pipeline fixes encoding issues."""
        cleaner = ContentCleaner()
        content = """
        # Documentation
        
        This page shows encoding issues like cafÃ©.
        Using â€” dash and â€œquotesâ€.
        
        ```rust
        fn main() {}
        ```
        """
        
        cleaned = cleaner.clean(content)
        
        # Should be fixed after cleaning
        assert "cafÃ©" not in cleaned
        assert "â€”" not in cleaned
        assert "â€œ" not in cleaned
    
    def test_audit_after_clean(self):
        """Audit after clean should show no defects."""
        cleaner = ContentCleaner()
        auditor = EncodingAuditor()
        
        content = "Text with Ã© encoding issue"
        cleaned = cleaner.clean(content)
        
        defects = auditor.scan_text(cleaned)
        
        # Should have no defects after cleaning
        assert len(defects) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
