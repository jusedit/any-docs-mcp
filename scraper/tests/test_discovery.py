"""Unit tests for discovery.py — canonicalization, navigability, sitemap parsing."""
from discovery import DiscoveryWorker


class TestCanonicalize:
    def setup_method(self):
        self.worker = DiscoveryWorker()

    def test_strips_trailing_slash(self):
        result = self.worker._canonicalize("https://example.com/docs/", "https://example.com")
        assert result == "https://example.com/docs"

    def test_root_stays_slash(self):
        result = self.worker._canonicalize("https://example.com/", "https://example.com")
        assert result == "https://example.com/"

    def test_relative_url_resolved(self):
        result = self.worker._canonicalize("/docs/intro", "https://example.com")
        assert result == "https://example.com/docs/intro"

    def test_empty_url_returns_none(self):
        result = self.worker._canonicalize("", "https://example.com")
        assert result is None

    def test_preserves_scheme_and_host(self):
        result = self.worker._canonicalize("https://example.com/a/b/c", "https://example.com")
        assert result == "https://example.com/a/b/c"


class TestIsNavigable:
    def test_html_is_navigable(self):
        assert DiscoveryWorker._is_navigable("https://example.com/docs/intro")

    def test_pdf_not_navigable(self):
        assert not DiscoveryWorker._is_navigable("https://example.com/file.pdf")

    def test_image_not_navigable(self):
        assert not DiscoveryWorker._is_navigable("https://example.com/logo.png")

    def test_css_not_navigable(self):
        assert not DiscoveryWorker._is_navigable("https://example.com/style.css")

    def test_js_not_navigable(self):
        assert not DiscoveryWorker._is_navigable("https://example.com/app.js")

    def test_html_extension_navigable(self):
        assert DiscoveryWorker._is_navigable("https://example.com/page.html")
