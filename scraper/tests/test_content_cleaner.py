"""Unit tests for content_cleaner.py."""
from content_cleaner import ContentCleaner


class TestCodeBlockLanguages:
    def setup_method(self):
        self.cleaner = ContentCleaner()

    def test_css_class_to_language(self):
        content = "```language-js\nconsole.log('hi');\n```"
        result = self.cleaner.clean(content)
        assert "```javascript" in result

    def test_bad_language_removed(self):
        content = "```sp-pre-placeholder\ncode here\n```"
        result = self.cleaner.clean(content)
        assert "sp-pre-placeholder" not in result

    def test_normalize_to_lowercase(self):
        content = "```Python\nprint('hi')\n```"
        result = self.cleaner.clean(content)
        assert "```python" in result

    def test_shell_variants_normalized(self):
        content = "```sh\necho hello\n```"
        result = self.cleaner.clean(content)
        assert "```bash" in result


class TestUIArtifacts:
    def setup_method(self):
        self.cleaner = ContentCleaner()

    def test_copy_to_clipboard_removed(self):
        content = "Some code\nCopy to clipboard\nMore text"
        result = self.cleaner.clean(content)
        assert "Copy to clipboard" not in result

    def test_edit_on_github_removed(self):
        content = "# Title\n[Edit on GitHub](https://github.com/example)\nContent"
        result = self.cleaner.clean(content)
        assert "Edit on GitHub" not in result

    def test_cookie_consent_removed(self):
        content = "Content\nWe use cookies\nMore content"
        result = self.cleaner.clean(content)
        assert "We use cookies" not in result

    def test_on_this_page_removed(self):
        content = "# Title\nOn this page\nActual content"
        result = self.cleaner.clean(content)
        assert "On this page" not in result


class TestEncoding:
    def setup_method(self):
        self.cleaner = ContentCleaner()

    def test_smart_quotes_fixed(self):
        content = "It\u2019s a \u201ctest\u201d"
        result = self.cleaner.clean(content)
        assert "It's" in result
        assert '"test"' in result

    def test_em_dash_fixed(self):
        content = "word\u2014word"
        result = self.cleaner.clean(content)
        assert "word--word" in result


class TestPermalinkAnchors:
    def setup_method(self):
        self.cleaner = ContentCleaner()

    def test_pilcrow_removed(self):
        content = "## Security\u00b6"
        result = self.cleaner.clean(content)
        assert result.strip() == "## Security"

    def test_pilcrow_link_removed(self):
        content = '## Security[\u00b6](#security "Permalink")'
        result = self.cleaner.clean(content)
        assert "\u00b6" not in result
        assert "Security" in result

    def test_empty_anchor_removed(self):
        content = "## Security[](#security)"
        result = self.cleaner.clean(content)
        assert "[](#security)" not in result


class TestDuplicateHeaders:
    def setup_method(self):
        self.cleaner = ContentCleaner()

    def test_consecutive_duplicates_removed(self):
        content = "## Title\n## Title\nContent"
        result = self.cleaner.clean(content)
        lines = [l for l in result.split("\n") if l.strip().startswith("##")]
        assert len(lines) == 1

    def test_non_consecutive_deduped(self):
        content = "## Title\nSome text\n## Title"
        result = self.cleaner.clean(content)
        lines = [l for l in result.split("\n") if l.strip().startswith("##")]
        assert len(lines) == 1

    def test_different_headings_kept(self):
        content = "## Title A\nSome text\n## Title B"
        result = self.cleaner.clean(content)
        lines = [l for l in result.split("\n") if l.strip().startswith("##")]
        assert len(lines) == 2


class TestWhitespace:
    def setup_method(self):
        self.cleaner = ContentCleaner()

    def test_excessive_newlines_collapsed(self):
        content = "Line 1\n\n\n\n\n\nLine 2"
        result = self.cleaner.clean(content)
        assert "\n\n\n\n" not in result
        assert "Line 1" in result
        assert "Line 2" in result

    def test_trailing_whitespace_removed(self):
        content = "Line with spaces   \nAnother line  "
        result = self.cleaner.clean(content)
        for line in result.split("\n"):
            assert line == line.rstrip()


class TestEmptyCodeBlocks:
    def setup_method(self):
        self.cleaner = ContentCleaner()

    def test_empty_block_removed(self):
        content = "Before\n```python\n```\nAfter"
        result = self.cleaner.clean(content)
        assert "```" not in result

    def test_whitespace_only_block_removed(self):
        content = "Before\n```\n   \n```\nAfter"
        result = self.cleaner.clean(content)
        assert "```" not in result
