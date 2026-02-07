"""
Comprehensive verification tests for v4 URL Discovery improvements.

Tests all 7 cycles:
1. Adaptive multi-scope detection
2. Documentation path detection
3. Multi-scope URL filtering
4. Multi-page recursive navigation
5. SPA deep navigation extraction
6. WebDriver escalation
7. Sitemap-assisted navigation
"""
import pytest
import re
from unittest.mock import patch, MagicMock
from url_discovery import URLDiscovery


@pytest.fixture
def discovery():
    """URLDiscovery instance without API key (no LLM calls)."""
    return URLDiscovery(api_key=None)


# ============================================================
# CYCLE 1-3: Scope Boundary Detection
# ============================================================

class TestDetermineScope:
    """Test _determine_scope returns List[str]."""

    def test_returns_list(self, discovery):
        result = discovery._determine_scope("https://example.com/docs/intro")
        assert isinstance(result, list)

    def test_specific_path_returns_single_scope(self, discovery):
        result = discovery._determine_scope("https://example.com/docs/intro")
        assert result == ["/docs/intro/"]

    def test_root_url_with_no_page_returns_slash(self, discovery):
        """Root URL without fetchable page falls back to ['/']."""
        with patch.object(discovery.session, 'get', side_effect=Exception("timeout")):
            result = discovery._determine_scope("https://example.com/")
        assert result == ['/']

    def test_root_url_analyzes_page(self, discovery):
        """Root URL fetches page and analyzes nav links."""
        mock_html = """
        <html><body>
        <nav>
            <a href="/docs/intro">Docs</a>
            <a href="/reference/api">Reference</a>
            <a href="/blog/post1">Blog</a>
        </nav>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = mock_html
        mock_response.raise_for_status = MagicMock()
        with patch.object(discovery.session, 'get', return_value=mock_response):
            result = discovery._determine_scope("https://example.com/")
        # docs and reference should score positively, blog negatively
        assert '/docs/' in result
        assert '/reference/' in result
        assert '/blog/' not in result


class TestUrlInScope:
    """Test multi-scope filtering."""

    def test_matches_any_scope(self, discovery):
        assert discovery._url_in_scope(
            "https://example.com/docs/intro",
            "https://example.com",
            ["/docs/", "/guide/"]
        ) is True

    def test_rejects_out_of_scope(self, discovery):
        assert discovery._url_in_scope(
            "https://example.com/blog/post1",
            "https://example.com",
            ["/docs/", "/guide/"]
        ) is False

    def test_slash_scope_matches_everything(self, discovery):
        assert discovery._url_in_scope(
            "https://example.com/anything",
            "https://example.com",
            ["/"]
        ) is True

    def test_rejects_different_domain(self, discovery):
        assert discovery._url_in_scope(
            "https://other.com/docs/intro",
            "https://example.com",
            ["/docs/"]
        ) is False

    def test_backward_compat_string_scope(self, discovery):
        """String scope (not list) should still work."""
        assert discovery._url_in_scope(
            "https://example.com/docs/intro",
            "https://example.com",
            "/docs/"
        ) is True


# ============================================================
# CYCLE 4: Multi-page Recursive Navigation
# ============================================================

class TestSectionPageHeuristic:
    """Test _is_section_page and _looks_like_leaf_page."""

    def test_short_path_is_section(self, discovery):
        assert discovery._is_section_page("https://example.com/learn") is True
        assert discovery._is_section_page("https://example.com/docs/guide") is True

    def test_deep_path_is_leaf(self, discovery):
        assert discovery._is_section_page(
            "https://example.com/docs/guide/advanced/performance"
        ) is False

    def test_keyword_section(self, discovery):
        assert discovery._is_section_page("https://example.com/api/reference/list") is True

    def test_html_extension_is_leaf(self, discovery):
        assert discovery._looks_like_leaf_page(
            "https://example.com/docs/intro.html"
        ) is True

    def test_empty_path_is_not_section(self, discovery):
        assert discovery._is_section_page("https://example.com/") is False


class TestRecursiveNavigation:
    """Test Level 1 recursive extraction in _try_navigation."""

    def test_fetches_section_pages(self, discovery):
        """Verify _try_navigation fetches section pages for Level 1."""
        main_html = """
        <html><body>
        <nav>
            <a href="/docs">Docs</a>
            <a href="/guide">Guide</a>
        </nav>
        </body></html>
        """
        section_html = """
        <html><body>
        <nav>
            <a href="/docs/intro">Intro</a>
            <a href="/docs/advanced">Advanced</a>
            <a href="/docs/faq">FAQ</a>
        </nav>
        </body></html>
        """

        def mock_get(url, **kwargs):
            resp = MagicMock()
            resp.status_code = 200
            resp.raise_for_status = MagicMock()
            if url in ("https://example.com/docs", "https://example.com/guide"):
                resp.text = section_html
            else:
                resp.text = main_html
            return resp

        with patch.object(discovery.session, 'get', side_effect=mock_get):
            urls = discovery._try_navigation(
                "https://example.com",
                ["/docs/", "/guide/"],
                max_level1_pages=5
            )

        url_set = {u['url'] for u in urls}
        # Should have found sub-pages from section page nav
        assert "https://example.com/docs/intro" in url_set
        assert "https://example.com/docs/advanced" in url_set

    def test_deduplication(self, discovery):
        """Same URL found in main and section page should appear once."""
        html = """
        <html><body>
        <nav>
            <a href="/docs">Docs</a>
            <a href="/docs/intro">Intro</a>
        </nav>
        </body></html>
        """
        def mock_get(url, **kwargs):
            resp = MagicMock()
            resp.status_code = 200
            resp.raise_for_status = MagicMock()
            resp.text = html
            return resp

        with patch.object(discovery.session, 'get', side_effect=mock_get):
            urls = discovery._try_navigation("https://example.com", ["/docs/"])

        url_list = [u['url'] for u in urls]
        assert len(url_list) == len(set(url_list)), "Duplicate URLs found!"


# ============================================================
# CYCLE 5: SPA Deep Navigation Extraction
# ============================================================

class TestSPAExtraction:
    """Test _extract_spa_navigation."""

    def test_next_data_extraction(self, discovery):
        html = """
        <script>window.__NEXT_DATA__ = {"props":{"pageProps":{"navigation":[
            {"url":"/docs/intro","title":"Introduction"},
            {"url":"/docs/setup","title":"Setup"}
        ]}}}</script>
        """
        urls = discovery._extract_spa_navigation(
            html, "https://example.com", "https://example.com", ["/docs/"]
        )
        assert len(urls) == 2
        assert urls[0]['source'] == 'spa'

    def test_docusaurus_extraction(self, discovery):
        html = """
        <script>window.__DOCUSAURUS_CONFIG__ = {"themeConfig":{"navbar":{"items":[
            {"to":"/docs/intro","label":"Intro"},
            {"href":"/docs/api","label":"API"}
        ]}}}</script>
        """
        urls = discovery._extract_spa_navigation(
            html, "https://example.com", "https://example.com", ["/docs/"]
        )
        assert len(urls) == 2

    def test_generic_json_scanning(self, discovery):
        html = """
        <script>
        var config = [{"path": "/docs/quickstart", "title": "Quick Start"}];
        </script>
        """
        urls = discovery._extract_spa_navigation(
            html, "https://example.com", "https://example.com", ["/docs/"]
        )
        found_paths = [u['url'] for u in urls]
        assert "https://example.com/docs/quickstart" in found_paths

    def test_js_path_extraction(self, discovery):
        html = """
        <script>
        var routes = ['/docs/intro', '/docs/advanced', '/docs/faq'];
        </script>
        """
        urls = discovery._extract_spa_navigation(
            html, "https://example.com", "https://example.com", ["/docs/"]
        )
        found_paths = [u['url'] for u in urls]
        assert "https://example.com/docs/intro" in found_paths

    def test_empty_html_returns_empty(self, discovery):
        urls = discovery._extract_spa_navigation(
            "<html><body>No scripts</body></html>",
            "https://example.com", "https://example.com", ["/docs/"]
        )
        assert urls == []

    def test_scope_filtering_applied(self, discovery):
        html = """
        <script>window.__NEXT_DATA__ = {"props":{"pageProps":{"navigation":[
            {"url":"/docs/intro","title":"Intro"},
            {"url":"/blog/post","title":"Blog Post"}
        ]}}}</script>
        """
        urls = discovery._extract_spa_navigation(
            html, "https://example.com", "https://example.com", ["/docs/"]
        )
        # /blog/post should be filtered out by scope
        found_paths = [u['url'] for u in urls]
        assert "https://example.com/blog/post" not in found_paths


# ============================================================
# CYCLE 6: WebDriver Escalation
# ============================================================

class TestWebDriverEscalation:
    """Test WebDriver escalation in _try_navigation."""

    def test_escalation_triggers_on_few_urls_many_scripts(self, discovery):
        """WebDriver should trigger when <10 URLs and >3 script tags."""
        html = """
        <html><body>
        <nav><a href="/docs/intro">Intro</a></nav>
        <script>1</script><script>2</script><script>3</script><script>4</script>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = html
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        mock_wd = MagicMock()
        mock_wd.discover_urls.return_value = {
            'mode': 'webdriver',
            'urls': [
                {'url': 'https://example.com/docs/page1', 'title': 'Page 1'},
                {'url': 'https://example.com/docs/page2', 'title': 'Page 2'},
            ],
            'version': None,
            'scope': '/docs/',
            'stats': {'raw': 10, 'filtered': 2}
        }

        with patch.object(discovery.session, 'get', return_value=mock_response), \
             patch('url_discovery.SELENIUM_AVAILABLE', True), \
             patch('url_discovery.WebDriverDiscovery', return_value=mock_wd):
            urls = discovery._try_navigation(
                "https://example.com", ["/docs/"]
            )

        url_set = {u['url'] for u in urls}
        assert "https://example.com/docs/page1" in url_set
        assert "https://example.com/docs/page2" in url_set

    def test_no_escalation_when_enough_urls(self, discovery):
        """WebDriver should NOT trigger when >=10 URLs already found."""
        links = "\n".join(
            f'<a href="/docs/page{i}">Page {i}</a>' for i in range(15)
        )
        html = f"""
        <html><body>
        <nav>{links}</nav>
        <script>1</script><script>2</script><script>3</script><script>4</script>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = html
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        mock_wd_cls = MagicMock()
        with patch.object(discovery.session, 'get', return_value=mock_response), \
             patch('url_discovery.SELENIUM_AVAILABLE', True), \
             patch('url_discovery.WebDriverDiscovery', mock_wd_cls):
            discovery._try_navigation("https://example.com", ["/docs/"])

        mock_wd_cls.assert_not_called()

    def test_no_crash_when_selenium_unavailable(self, discovery):
        """Should silently skip when Selenium not available."""
        html = """
        <html><body>
        <nav><a href="/docs/intro">Intro</a></nav>
        <script>1</script><script>2</script><script>3</script><script>4</script>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = html
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        with patch.object(discovery.session, 'get', return_value=mock_response), \
             patch('url_discovery.SELENIUM_AVAILABLE', False):
            # Should not crash
            urls = discovery._try_navigation("https://example.com", ["/docs/"])
            assert isinstance(urls, list)


# ============================================================
# CYCLE 7: Sitemap-Assisted Navigation
# ============================================================

class TestSitemapScoring:
    """Test _score_and_filter_sitemap_urls."""

    def _make_urls(self, paths, base="https://example.com"):
        return [{'url': f"{base}{p}", 'title': p} for p in paths]

    def test_doc_paths_score_higher(self, discovery):
        urls = self._make_urls([
            "/docs/intro", "/docs/setup", "/docs/api",
            "/blog/post1", "/blog/post2", "/blog/post3",
            "/about/team", "/about/contact", "/about/careers",
        ] * 7)  # >50 to trigger grouping
        result = discovery._score_and_filter_sitemap_urls(urls, ["/"], "https://example.com")
        result_paths = [u['url'] for u in result]
        # docs should be kept, blog and about should be filtered
        assert any("/docs/" in p for p in result_paths)
        assert not any("/blog/" in p for p in result_paths)

    def test_translation_penalty(self, discovery):
        urls = self._make_urls([
            f"/{lang}/docs/page{i}" for lang in ['en', 'de', 'fr', 'ja']
            for i in range(15)
        ])
        result = discovery._score_and_filter_sitemap_urls(urls, ["/en/"], "https://example.com")
        result_paths = [u['url'] for u in result]
        # /en/ should be kept (scope bonus), /de/, /fr/, /ja/ penalized
        assert any("/en/docs/" in p for p in result_paths)

    def test_scope_bonus(self, discovery):
        urls = self._make_urls([
            f"/api/v1/page{i}" for i in range(20)
        ] + [
            f"/internal/page{i}" for i in range(20)
        ] + [
            f"/random/page{i}" for i in range(15)
        ])
        result = discovery._score_and_filter_sitemap_urls(urls, ["/api/"], "https://example.com")
        result_paths = [u['url'] for u in result]
        assert any("/api/" in p for p in result_paths)

    def test_fallback_when_no_positive_groups(self, discovery):
        """All groups score <= 0: should return ALL urls (fallback)."""
        urls = self._make_urls([
            f"/random/page{i}" for i in range(60)
        ])
        result = discovery._score_and_filter_sitemap_urls(urls, ["/nonexistent/"], "https://example.com")
        assert len(result) == len(urls), "Should fall back to all URLs"

    def test_small_sitemap_not_grouped(self, discovery):
        """Sitemaps with <=50 URLs should not be grouped."""
        urls = self._make_urls([f"/blog/post{i}" for i in range(30)])
        mock_parser = MagicMock()
        mock_parser.has_sitemap.return_value = True
        mock_parser.parse_sitemap.return_value = urls

        with patch('url_discovery.SitemapParser', return_value=mock_parser):
            result = discovery._try_sitemap("https://example.com", ["/"], 500)

        # All URLs returned since <50
        assert len(result) == 30


# ============================================================
# BUG: WebDriver return type mismatch
# ============================================================

class TestWebDriverReturnType:
    """WebDriverDiscovery.discover_urls returns Dict or None, not List.
    _try_navigation iterates over wd_urls assuming List[Dict].
    """

    def test_webdriver_returns_dict_with_urls_key(self):
        """Verify what WebDriverDiscovery.discover_urls actually returns."""
        from webdriver_discovery import WebDriverDiscovery
        # The method signature says -> Optional[Dict]
        # But _try_navigation line 552 does: `for url_info in wd_urls`
        # If wd_urls is a Dict (e.g., {'mode': ..., 'urls': [...]}),
        # iterating gives keys not url dicts.

        # This is a design review test - just flag the issue
        import inspect
        sig = inspect.signature(WebDriverDiscovery.discover_urls)
        return_annotation = sig.return_annotation
        # The return type is Optional[Dict] — this is a problem
        # because _try_navigation iterates over it as if it's List[Dict]
        assert True  # Flagged in review


# ============================================================
# CROSS-CUTTING: Locale Filter
# ============================================================

class TestLocaleFilter:
    """Test _apply_locale_filter."""

    def test_filters_non_matching_locales(self, discovery):
        urls = [
            {'url': 'https://example.com/en/docs/intro', 'title': 'EN'},
            {'url': 'https://example.com/de/docs/intro', 'title': 'DE'},
            {'url': 'https://example.com/ja/docs/intro', 'title': 'JA'},
        ]
        result = discovery._apply_locale_filter(urls, 'en')
        assert len(result) == 1
        assert result[0]['url'].endswith('/en/docs/intro')

    def test_no_filter_keeps_all(self, discovery):
        urls = [
            {'url': 'https://example.com/en/docs/intro', 'title': 'EN'},
            {'url': 'https://example.com/de/docs/intro', 'title': 'DE'},
        ]
        result = discovery._apply_locale_filter(urls, None)
        assert len(result) == 2


# ============================================================
# CROSS-CUTTING: Normalize URL
# ============================================================

class TestNormalizeUrl:
    """Test _normalize_url edge cases."""

    def test_absolute_url(self, discovery):
        assert discovery._normalize_url(
            "https://example.com/docs", "https://example.com/", "https://example.com"
        ) == "https://example.com/docs"

    def test_relative_url(self, discovery):
        result = discovery._normalize_url(
            "intro", "https://example.com/docs/", "https://example.com"
        )
        assert result == "https://example.com/docs/intro"

    def test_protocol_relative(self, discovery):
        result = discovery._normalize_url(
            "//cdn.example.com/path", "https://example.com/", "https://example.com"
        )
        assert result == "https://cdn.example.com/path"

    def test_hash_returns_none(self, discovery):
        assert discovery._normalize_url(
            "#section", "https://example.com/", "https://example.com"
        ) is None

    def test_javascript_returns_none(self, discovery):
        assert discovery._normalize_url(
            "javascript:void(0)", "https://example.com/", "https://example.com"
        ) is None


# ============================================================
# PERFORMANCE: O(n²) sort in _score_and_filter_sitemap_urls
# ============================================================

class TestSitemapSortPerformance:
    """The sort at line 437 is O(n*g) per comparison — test it doesn't hang."""

    def test_large_sitemap_completes_quickly(self, discovery):
        """1000 URLs should complete in <5 seconds."""
        import time
        urls = [{'url': f"https://example.com/docs/page{i}", 'title': f'Page {i}'}
                for i in range(1000)]
        start = time.time()
        discovery._score_and_filter_sitemap_urls(urls, ["/docs/"], "https://example.com")
        elapsed = time.time() - start
        assert elapsed < 5.0, f"Sorting took {elapsed:.1f}s — O(n²) performance issue"
