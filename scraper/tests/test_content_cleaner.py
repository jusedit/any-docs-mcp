"""Test content cleaner functionality."""
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


def test_fix_markdown_tables_adds_separator(cleaner):
    """Fix markdown tables missing separator row."""
    content = "| Header 1 | Header 2 |\n| Row 1 | Row 2 |"
    result = cleaner.fix_markdown_tables(content)
    assert "| --- |" in result or "|---|" in result


def test_fix_markdown_tables_preserves_valid_tables(cleaner):
    """Valid tables with separator are preserved."""
    content = "| Header 1 | Header 2 |\n| --- | --- |\n| Row 1 | Row 2 |"
    result = cleaner.fix_markdown_tables(content)
    assert result.count("Header 1") == 1  # No duplicate headers


def test_deduplicate_content_removes_duplicates(cleaner):
    """Remove duplicate paragraphs."""
    content = "Some paragraph with enough text to trigger deduplication.\n\nSome paragraph with enough text to trigger deduplication."
    result = cleaner.deduplicate_content(content)
    # Should keep only one copy
    assert result.count("Some paragraph") == 1


def test_auto_detect_code_language_python(cleaner):
    """Detect Python code blocks."""
    content = "```\ndef hello():\n    pass\n```"
    result = cleaner.fix_code_block_languages(content)
    assert "```python" in result


def test_auto_detect_code_language_bash(cleaner):
    """Detect Bash code blocks."""
    content = "```\n$ npm install\n```"
    result = cleaner.fix_code_block_languages(content)
    assert "```bash" in result


def test_remove_ui_artifacts_copy_button(cleaner):
    """Remove copy button artifacts."""
    content = "Some code\nCopy to clipboard\nMore content"
    result = cleaner.remove_ui_artifacts(content)
    assert "Copy to clipboard" not in result


def test_remove_ui_artifacts_codesandbox(cleaner):
    """Remove CodeSandbox button."""
    content = "Code example\n[Open in CodeSandbox](url)\nMore text"
    result = cleaner.remove_ui_artifacts(content)
    assert "Open in CodeSandbox" not in result
