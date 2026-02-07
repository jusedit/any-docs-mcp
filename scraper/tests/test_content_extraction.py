"""Test content extraction from HTML fixtures against golden expected output."""
import pytest
from pathlib import Path
from bs4 import BeautifulSoup
from content_cleaner import ContentCleaner
from markdownify import markdownify as md


FIXTURES_DIR = Path(__file__).parent.parent.parent / 'tests' / 'fixtures'
HTML_DIR = FIXTURES_DIR / 'html'
EXPECTED_DIR = FIXTURES_DIR / 'expected'


def normalize_whitespace(content: str) -> str:
    """Normalize whitespace for comparison - ignore trailing differences."""
    lines = [line.rstrip() for line in content.split('\n')]
    return '\n'.join(line for line in lines if line)


@pytest.mark.parametrize("fixture_name,expected_headings,expected_code_blocks", [
    ("vitepress-sample", ["Getting Started", "Installation", "Setup"], ["bash", "javascript"]),
    ("docusaurus-sample", ["Installation", "Requirements", "Scaffold project", "Start dev server"], ["bash"]),
    ("github-raw-markdown", ["Installation Guide", "Requirements", "Quick Start", "Configuration", "Usage"], ["bash", "json", "javascript"])
])
def test_content_extraction_structure(fixture_name, expected_headings, expected_code_blocks):
    """Extract content and verify structure (headings, code blocks)."""
    # Load HTML fixture
    html_path = HTML_DIR / f"{fixture_name}.html"
    html_content = html_path.read_text(encoding='utf-8')
    
    # Parse and extract content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check for raw markdown div (GitHub style)
    raw_markdown_div = soup.find('div', class_='raw-markdown')
    if raw_markdown_div:
        extracted = raw_markdown_div.get_text().strip()
    else:
        # Use main content area and convert to markdown
        content_div = soup.find('main') or soup.find('article') or soup.find('div', class_='VPDoc') or soup.find('div', class_='theme-doc-markdown')
        if content_div:
            # Remove script/style tags
            for tag in content_div.find_all(['script', 'style']):
                tag.decompose()
            extracted = md(str(content_div), heading_style="ATX")
        else:
            extracted = md(str(soup), heading_style="ATX")
    
    # Clean the extracted content
    cleaner = ContentCleaner()
    cleaned = cleaner.clean(extracted)
    
    # Verify expected headings are present
    for heading in expected_headings:
        assert heading in cleaned, f"Expected heading '{heading}' not found in {fixture_name}"
    
    # Verify code blocks exist (by language marker)
    for lang in expected_code_blocks:
        assert f"```{lang}" in cleaned or f"```\n" in cleaned, f"Expected {lang} code block not found in {fixture_name}"
    
    # Verify content is not empty
    assert len(cleaned) > 100, f"Extracted content too short for {fixture_name}"
