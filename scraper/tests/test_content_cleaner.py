"""Test content cleaner heading normalization."""
import pytest
from content_cleaner import ContentCleaner


@pytest.fixture
def cleaner():
    return ContentCleaner()


def test_normalize_heading_levels_fixes_deep_first_heading(cleaner):
    """First heading that is ### becomes ##."""
    content = "### Deep Heading\n\nSome text"
    result = cleaner.normalize_heading_levels(content)
    assert result.startswith("## Deep Heading")


def test_normalize_heading_levels_prevents_skipping(cleaner):
    """No jumping from ## to ####."""
    content = "## Level 2\n\n#### Level 4 (should be ###)"
    result = cleaner.normalize_heading_levels(content)
    assert "### Level 4" in result
    assert "#### Level 4" not in result


def test_normalize_heading_levels_allows_gradual_increase(cleaner):
    """Gradual increase ## -> ### is allowed."""
    content = "## Level 2\n\n### Level 3\n\n#### Level 4"
    result = cleaner.normalize_heading_levels(content)
    assert "## Level 2" in result
    assert "### Level 3" in result
    assert "#### Level 4" in result


def test_normalize_heading_levels_no_change_for_valid_structure(cleaner):
    """Valid heading structure is preserved."""
    content = "# Title\n\n## Section\n\n### Subsection"
    result = cleaner.normalize_heading_levels(content)
    assert "# Title" in result
    assert "## Section" in result
    assert "### Subsection" in result
