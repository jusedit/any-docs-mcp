"""Tests for HTML residue audit and Tailwind cleanup."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tests" / "e2e"))

from content_cleaner import ContentCleaner
from audit_html_residue import HTMLResidueAuditor


class TestHTMLResidueAuditor:
    """Test HTML residue audit functionality."""
    
    def test_detects_html_tags(self, tmp_path):
        """Auditor detects HTML tags in markdown."""
        auditor = HTMLResidueAuditor()
        test_file = tmp_path / "test.md"
        test_file.write_text("<div class='test'>Some content</div>\n\n## Heading\n\nMore text.")
        
        result = auditor.audit_file(test_file)
        
        assert result['residue_count'] > 0
        assert any(r['type'] == 'html_tag' for r in result['residues'])
    
    def test_detects_tailwind_classes(self, tmp_path):
        """Auditor detects Tailwind utility classes."""
        auditor = HTMLResidueAuditor()
        test_file = tmp_path / "test.md"
        test_file.write_text('<div class="bg-blue-500 text-white p-4">Styled content</div>')
        
        result = auditor.audit_file(test_file)
        
        assert result['residue_count'] > 0
        assert any(r['type'] == 'tailwind_class' for r in result['residues'])
    
    def test_counts_multiple_instances(self, tmp_path):
        """Auditor counts multiple HTML instances correctly."""
        auditor = HTMLResidueAuditor()
        test_file = tmp_path / "test.md"
        test_file.write_text("<div>1</div>\n<div>2</div>\n<div>3</div>")
        
        result = auditor.audit_file(test_file)
        
        assert result['residue_count'] == 6  # 3 opening + 3 closing tags


class TestTailwindCleanup:
    """Test Tailwind-specific cleanup in ContentCleaner."""
    
    def test_removes_utility_class_divs(self):
        """Tailwind profile removes utility class divs."""
        cleaner = ContentCleaner(site_type='tailwind')
        content = '<div class="bg-blue-500 text-white p-4 flex items-center">Important content</div>'
        
        cleaned = cleaner.clean(content)
        
        assert 'bg-blue-500' not in cleaned
        assert 'flex items-center' not in cleaned
    
    def test_removes_color_swatches(self):
        """Tailwind profile removes color swatches."""
        cleaner = ContentCleaner(site_type='tailwind')
        content = '[#3b82f6](blue) and [#ef4444](red)'
        
        cleaned = cleaner.clean(content)
        
        assert '#3b82f6' not in cleaned
        assert '#ef4444' not in cleaned
    
    def test_removes_try_it_links(self):
        """Tailwind profile removes 'Try it' playground links."""
        cleaner = ContentCleaner(site_type='tailwind')
        content = '[Try it](https://play.tailwindcss.com/test)'
        
        cleaned = cleaner.clean(content)
        
        assert 'play.tailwindcss.com' not in cleaned
    
    def test_preserves_valid_content(self):
        """Tailwind profile preserves valid markdown content."""
        cleaner = ContentCleaner(site_type='tailwind')
        content = "## Important Section\n\nThis is valid content with `code` and **bold** text."
        
        cleaned = cleaner.clean(content)
        
        assert 'Important Section' in cleaned
        assert 'valid content' in cleaned


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
