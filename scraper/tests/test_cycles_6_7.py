"""Tests for Cycles 6 & 7: Permalink removal and Pattern discovery."""
import pytest
from pathlib import Path

from content_cleaner import ContentCleaner
from pattern_discovery import discover_patterns, is_likely_boilerplate, PatternCandidate


class TestPermalinkRemoval:
    """Cycle 6: Tests for remove_permalink_anchors."""
    
    def test_removes_trailing_permalink_char(self):
        """Removes trailing ¶ from headings."""
        cleaner = ContentCleaner()
        content = "## Security¶"
        result = cleaner.remove_permalink_anchors(content)
        assert "## Security" in result
        assert "¶" not in result
    
    def test_removes_permalink_link(self):
        """Removes [¶](#anchor) from headings."""
        cleaner = ContentCleaner()
        content = '## OAuth2[¶](#oauth2 "link")'
        result = cleaner.remove_permalink_anchors(content)
        assert "## OAuth2" in result
        assert "[¶]" not in result
    
    def test_removes_empty_anchor_link(self):
        """Removes []( #anchor) from headings."""
        cleaner = ContentCleaner()
        content = "### OpenID[]( #openid)"
        result = cleaner.remove_permalink_anchors(content)
        assert "### OpenID" in result
        assert "[]" not in result
    
    def test_preserves_inline_code_in_headings(self):
        """Preserves inline code while removing permalink."""
        cleaner = ContentCleaner()
        content = "## Using `async`[Â¶](#using-async)"
        result = cleaner.remove_permalink_anchors(content)
        assert "## Using `async`" in result
        assert "`async`" in result
    
    def test_preserves_non_heading_lines(self):
        """Non-heading lines are unchanged."""
        cleaner = ContentCleaner()
        content = "This line has Â¶ in content"
        result = cleaner.remove_permalink_anchors(content)
        assert "Â¶" in result  # Not removed in non-heading


class TestPatternDiscovery:
    """Cycle 7: Tests for pattern discovery."""
    
    def test_discovers_repeated_patterns(self, tmp_path):
        """Discovers patterns appearing in multiple files."""
        # Create files with repeated content
        (tmp_path / "file1.md").write_text("Show more\n\nContent here")
        (tmp_path / "file2.md").write_text("Show more\n\nOther content")
        (tmp_path / "file3.md").write_text("Show more\n\nMore content")
        
        candidates = discover_patterns(str(tmp_path), threshold=0.3, min_occurrences=2)
        
        # Should find "Show more"
        patterns = [c.pattern for c in candidates]
        assert any("Show more" in p for p in patterns)
    
    def test_respects_threshold(self, tmp_path):
        """Only returns patterns above threshold."""
        # Create 10 files, pattern in only 1
        for i in range(10):
            (tmp_path / f"file{i}.md").write_text(f"Content {i}")
        (tmp_path / "special.md").write_text("Unique pattern here")
        
        candidates = discover_patterns(str(tmp_path), threshold=0.3)
        
        # "Unique pattern" appears in only 1/11 files (< 30%)
        patterns = [c.pattern for c in candidates]
        assert not any("Unique pattern" in p for p in patterns)
    
    def test_returns_pattern_candidates(self, tmp_path):
        """Returns PatternCandidate objects."""
        (tmp_path / "file.md").write_text("Show more")
        
        candidates = discover_patterns(str(tmp_path), threshold=0.0, min_occurrences=1)
        
        if candidates:
            assert isinstance(candidates[0], PatternCandidate)
            assert hasattr(candidates[0], 'count')
            assert hasattr(candidates[0], 'suggested_regex')
    
    def test_boilerplate_detection(self):
        """Identifies likely boilerplate lines."""
        assert is_likely_boilerplate("Show more")
        assert is_likely_boilerplate("Cookie Policy")
        assert is_likely_boilerplate("Back to top")
        assert not is_likely_boilerplate("Introduction to Python")
        assert not is_likely_boilerplate("## Getting Started")
