"""Tests for heading hierarchy normalization."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))

from content_cleaner import ContentCleaner


class TestHeadingHierarchyNormalization:
    """Test heading hierarchy normalization."""
    
    def test_first_heading_normalized_to_h1_or_h2(self):
        """First heading is normalized to # or ##."""
        cleaner = ContentCleaner()
        content = "### Third Level Heading\n\nSome text."
        
        normalized = cleaner.normalize_heading_levels(content)
        
        # Should start with ## (h2) not ### (h3)
        assert normalized.startswith("## Third Level Heading")
        assert "### Third Level Heading" not in normalized
    
    def test_no_level_skipping(self):
        """No skipped heading levels (h1 -> h3 without h2)."""
        cleaner = ContentCleaner()
        content = "# Title\n\n### Skipped Level\n\nSome text."
        
        normalized = cleaner.normalize_heading_levels(content)
        
        # h3 should become h2 since we skipped h2
        assert "## Skipped Level" in normalized
        assert "### Skipped Level" not in normalized
    
    def test_multiple_h1_normalized(self):
        """Multiple h1 headings are cleaned."""
        cleaner = ContentCleaner()
        content = "# First Title\n\n# Second Title\n\nText."
        
        normalized = cleaner.normalize_heading_levels(content)
        
        # Should have both h1s (for now - future enhancement could make second h2)
        assert "# First Title" in normalized
        assert "# Second Title" in normalized
    
    def test_subsections_allowed(self):
        """Subsections with same level are allowed."""
        cleaner = ContentCleaner()
        content = "## Section\n\n### Subsection 1\n\n### Subsection 2\n\nText."
        
        normalized = cleaner.normalize_heading_levels(content)
        
        # Both subsections should remain at h3
        assert "### Subsection 1" in normalized
        assert "### Subsection 2" in normalized
    
    def test_heading_text_preserved(self):
        """Heading text is preserved during normalization."""
        cleaner = ContentCleaner()
        content = "#### My Special Heading\n\nContent."
        
        normalized = cleaner.normalize_heading_levels(content)
        
        assert "My Special Heading" in normalized
    
    def test_complex_hierarchy(self):
        """Complex heading hierarchies are normalized."""
        cleaner = ContentCleaner()
        content = """
# Title

## Section 1

#### Deeply Nested

## Section 2

### Subsection

##### Very Deep
"""
        
        normalized = cleaner.normalize_heading_levels(content)
        
        # First heading is # (h1) - correct
        assert "# Title" in normalized
        
        # h4 should become h3 (no skipping from h2)
        assert "### Deeply Nested" in normalized
        assert "#### Deeply Nested" not in normalized
        
        # h3 should remain h3
        assert "### Subsection" in normalized
        
        # h5 should become h4 (no skipping)
        assert "#### Very Deep" in normalized
        assert "##### Very Deep" not in normalized
    
    def test_non_heading_lines_unchanged(self):
        """Non-heading lines are not modified."""
        cleaner = ContentCleaner()
        content = "Some text\n\n## Heading\n\nMore text."
        
        normalized = cleaner.normalize_heading_levels(content)
        
        assert "Some text" in normalized
        assert "More text." in normalized
        assert "## Heading" in normalized


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
