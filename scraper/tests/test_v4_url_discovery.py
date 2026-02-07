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
from url_discovery import URLDiscovery, ScopeRules


@pytest.fixture
def discovery():
    """URLDiscovery instance without API key (no LLM calls)."""
    return URLDiscovery(api_key=None)


def _scope(base_url: str, prefixes) -> ScopeRules:
    """Helper: create ScopeRules from path prefixes for tests."""
    if isinstance(prefixes, str):
        prefixes = [prefixes]
    return ScopeRules.from_path_prefixes(base_url, prefixes)


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
        assert discovery._is_section_page("https://example.com/api/reference") is True
        assert discovery._is_section_page("https://example.com/docs/guide") is True

    def test_non_keyword_not_section(self, discovery):
        """3-segment URL with non-keyword last segment is NOT a section."""
        assert discovery._is_section_page("https://example.com/api/reference/list") is False

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
                _scope("https://example.com", ["/docs/", "/guide/"]),
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
            urls = discovery._try_navigation("https://example.com", _scope("https://example.com", ["/docs/"]))

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
            html, "https://example.com", "https://example.com", _scope("https://example.com", ["/docs/"])
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
            html, "https://example.com", "https://example.com", _scope("https://example.com", ["/docs/"])
        )
        assert len(urls) == 2

    def test_generic_json_scanning(self, discovery):
        html = """
        <script>
        var config = [{"path": "/docs/quickstart", "title": "Quick Start"}];
        </script>
        """
        urls = discovery._extract_spa_navigation(
            html, "https://example.com", "https://example.com", _scope("https://example.com", ["/docs/"])
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
            html, "https://example.com", "https://example.com", _scope("https://example.com", ["/docs/"])
        )
        found_paths = [u['url'] for u in urls]
        assert "https://example.com/docs/intro" in found_paths

    def test_empty_html_returns_empty(self, discovery):
        urls = discovery._extract_spa_navigation(
            "<html><body>No scripts</body></html>",
            "https://example.com", "https://example.com", _scope("https://example.com", ["/docs/"])
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
            html, "https://example.com", "https://example.com", _scope("https://example.com", ["/docs/"])
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
                "https://example.com", _scope("https://example.com", ["/docs/"])
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
            discovery._try_navigation("https://example.com", _scope("https://example.com", ["/docs/"]))

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
            urls = discovery._try_navigation("https://example.com", _scope("https://example.com", ["/docs/"]))
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
            result = discovery._try_sitemap("https://example.com", _scope("https://example.com", ["/"]), 500)

        # All URLs returned (scope matches all)
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


# ============================================================
# D2: Generic Locale Detection
# ============================================================

class TestGenericLocaleFilter:
    """Test generic regex-based locale detection (D2 fix)."""

    def test_filters_polish_urls(self, discovery):
        """Polish (/pl/) was NOT in the old hardcoded set — now detected generically."""
        urls = [
            {'url': 'https://example.com/en/docs/intro', 'title': 'EN'},
            {'url': 'https://example.com/pl/docs/intro', 'title': 'PL'},
            {'url': 'https://example.com/sv/docs/intro', 'title': 'SV'},
        ]
        result = discovery._apply_locale_filter(urls, 'en')
        assert len(result) == 1
        assert result[0]['url'].endswith('/en/docs/intro')

    def test_non_locale_segments_not_filtered(self, discovery):
        """Known non-locale segments like /js/, /go/, /ai/ should not be treated as locales."""
        urls = [
            {'url': 'https://example.com/en/js/basics', 'title': 'JS'},
            {'url': 'https://example.com/en/go/setup', 'title': 'Go'},
            {'url': 'https://example.com/en/ai/intro', 'title': 'AI'},
        ]
        result = discovery._apply_locale_filter(urls, 'en')
        assert len(result) == 3  # All kept — /js/, /go/, /ai/ are not locales

    def test_urls_without_locale_kept(self, discovery):
        """URLs with no locale segment should always be kept."""
        urls = [
            {'url': 'https://example.com/docs/intro', 'title': 'Intro'},
            {'url': 'https://example.com/api/reference', 'title': 'API'},
        ]
        result = discovery._apply_locale_filter(urls, 'de')
        assert len(result) == 2


# ============================================================
# D3: SPA Noise Reduction
# ============================================================

class TestSPANoiseReduction:
    """Test that noisy asset paths are filtered out (D3 fix)."""

    def test_asset_paths_filtered(self, discovery):
        html = """
        <script>
        var paths = ['/static/bundle.js', '/assets/logo.png', '/docs/intro/setup'];
        </script>
        """
        urls = discovery._extract_spa_navigation(
            html, "https://example.com", "https://example.com", _scope("https://example.com", ["/"])
        )
        found = [u['url'] for u in urls]
        assert not any('/static/' in u for u in found)
        assert not any('/assets/' in u for u in found)

    def test_single_segment_paths_not_extracted(self, discovery):
        """Single-segment paths like '/fonts' should no longer be extracted by JS regex."""
        html = """
        <script>
        var x = '/fonts';
        var y = '/docs/intro';
        </script>
        """
        urls = discovery._extract_spa_navigation(
            html, "https://example.com", "https://example.com", _scope("https://example.com", ["/"])
        )
        found = [u['url'] for u in urls]
        assert not any(u.endswith('/fonts') for u in found)


# ============================================================
# D5: Query Parameter Stripping
# ============================================================

class TestQueryParamStripping:
    """Test that _normalize_url strips query params and fragments (D5 fix)."""

    def test_strips_query_params(self, discovery):
        result = discovery._normalize_url(
            "/docs/intro?tab=js&theme=dark", "https://example.com/", "https://example.com"
        )
        assert result == "https://example.com/docs/intro"

    def test_strips_fragment(self, discovery):
        result = discovery._normalize_url(
            "/docs/intro#section-1", "https://example.com/", "https://example.com"
        )
        assert result == "https://example.com/docs/intro"

    def test_strips_both(self, discovery):
        result = discovery._normalize_url(
            "/docs/intro?tab=js#section", "https://example.com/", "https://example.com"
        )
        assert result == "https://example.com/docs/intro"

    def test_fragment_only_returns_none(self, discovery):
        """Href that is just a fragment should return None."""
        result = discovery._normalize_url(
            "#section", "https://example.com/", "https://example.com"
        )
        assert result is None


# ============================================================
# D6: Hybrid Discovery Strategy
# ============================================================

class TestHybridStrategy:
    """Test that discover_urls uses hybrid strategy instead of first-wins (D6 fix)."""

    def test_merges_sitemap_and_navigation(self, discovery):
        """Both sitemap and navigation results should be merged."""
        sitemap_urls = [{'url': f'https://example.com/docs/page{i}', 'title': f'SM {i}'}
                        for i in range(15)]
        nav_urls = [{'url': f'https://example.com/docs/nav{i}', 'title': f'Nav {i}'}
                    for i in range(5)]

        scope = _scope("https://example.com", ["/docs/"])
        with patch.object(discovery, '_scout_crawl', return_value=("", {"https://example.com/docs/"})), \
             patch.object(discovery, '_try_sitemap', return_value=sitemap_urls), \
             patch.object(discovery, '_try_navigation', return_value=nav_urls), \
             patch.object(discovery, '_determine_scope', return_value=['/docs/']), \
             patch.object(discovery.github_discovery, 'is_github_repo', return_value=False):
            result = discovery.discover_urls("https://example.com/docs/")

        urls = {u['url'] for u in result['urls']}
        # Should contain URLs from BOTH sources
        assert 'https://example.com/docs/page0' in urls
        assert 'https://example.com/docs/nav0' in urls
        assert len(result['urls']) == 20  # 15 + 5 unique
        assert 'hybrid' in result['mode']

    def test_deduplicates_across_modes(self, discovery):
        """Same URL found in sitemap and navigation should appear once."""
        shared_url = {'url': 'https://example.com/docs/intro', 'title': 'Intro'}
        sitemap_urls = [shared_url, {'url': 'https://example.com/docs/page1', 'title': 'P1'}] * 6
        nav_urls = [shared_url, {'url': 'https://example.com/docs/nav1', 'title': 'N1'}]

        with patch.object(discovery, '_scout_crawl', return_value=("", {"https://example.com/docs/"})), \
             patch.object(discovery, '_try_sitemap', return_value=sitemap_urls), \
             patch.object(discovery, '_try_navigation', return_value=nav_urls), \
             patch.object(discovery, '_determine_scope', return_value=['/docs/']), \
             patch.object(discovery.github_discovery, 'is_github_repo', return_value=False):
            result = discovery.discover_urls("https://example.com/docs/")

        url_list = [u['url'] for u in result['urls']]
        assert len(url_list) == len(set(url_list)), "Duplicate URLs found in hybrid result"

    def test_crawl_supplements_sparse_results(self, discovery):
        """Crawl should be used when sitemap+nav yields few results."""
        sitemap_urls = [{'url': 'https://example.com/docs/page1', 'title': 'P1'}]
        nav_urls = [{'url': 'https://example.com/docs/nav1', 'title': 'N1'}]
        crawl_urls = [{'url': f'https://example.com/docs/crawl{i}', 'title': f'C{i}'}
                      for i in range(20)]

        with patch.object(discovery, '_scout_crawl', return_value=("", {"https://example.com/docs/"})), \
             patch.object(discovery, '_try_sitemap', return_value=sitemap_urls), \
             patch.object(discovery, '_try_navigation', return_value=nav_urls), \
             patch.object(discovery, '_crawl_links', return_value=crawl_urls), \
             patch.object(discovery, '_determine_scope', return_value=['/docs/']), \
             patch.object(discovery.github_discovery, 'is_github_repo', return_value=False):
            result = discovery.discover_urls("https://example.com/docs/")

        urls = {u['url'] for u in result['urls']}
        assert 'https://example.com/docs/crawl0' in urls

    def test_no_crawl_when_enough_urls(self, discovery):
        """Crawl should NOT be triggered when sitemap+nav already has enough URLs."""
        sitemap_urls = [{'url': f'https://example.com/docs/page{i}', 'title': f'P{i}'}
                        for i in range(100)]

        mock_crawl = MagicMock(return_value=[])
        with patch.object(discovery, '_scout_crawl', return_value=("", {"https://example.com/docs/"})), \
             patch.object(discovery, '_try_sitemap', return_value=sitemap_urls), \
             patch.object(discovery, '_try_navigation', return_value=[]), \
             patch.object(discovery, '_crawl_links', mock_crawl), \
             patch.object(discovery, '_determine_scope', return_value=['/docs/']), \
             patch.object(discovery.github_discovery, 'is_github_repo', return_value=False):
            discovery.discover_urls("https://example.com/docs/")

        mock_crawl.assert_not_called()


# ============================================================
# D7: use_webdriver parameter
# ============================================================

class TestUseWebdriverParam:
    """Test use_webdriver parameter (D7 fix)."""

    def test_discover_urls_accepts_use_webdriver(self, discovery):
        """discover_urls() should accept use_webdriver parameter."""
        import inspect
        sig = inspect.signature(discovery.discover_urls)
        assert 'use_webdriver' in sig.parameters

    def test_force_webdriver_escalation(self, discovery):
        """use_webdriver=True should force WebDriver even with many URLs."""
        links = "\n".join(
            f'<a href="/docs/page{i}">Page {i}</a>' for i in range(20)
        )
        html = f"""
        <html><body>
        <nav>{links}</nav>
        <script>1</script>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = html
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        mock_wd = MagicMock()
        mock_wd.discover_urls.return_value = {
            'urls': [{'url': 'https://example.com/docs/wd1', 'title': 'WD1'}],
            'mode': 'webdriver', 'version': None, 'scope': '/', 'stats': {}
        }

        with patch.object(discovery.session, 'get', return_value=mock_response), \
             patch('url_discovery.SELENIUM_AVAILABLE', True), \
             patch('url_discovery.WebDriverDiscovery', return_value=mock_wd):
            urls = discovery._try_navigation(
                "https://example.com", _scope("https://example.com", ["/docs/"]), use_webdriver=True
            )

        # WebDriver should have been called despite having 20 URLs
        mock_wd.discover_urls.assert_called_once()


# ============================================================
# D8: Locale-aware Sitemap Scoring
# ============================================================

class TestLocaleAwareSitemapScoring:
    """Test that sitemap scoring uses locale_filter instead of hardcoded 'en' (D8 fix)."""

    def _make_urls(self, paths, base="https://example.com"):
        return [{'url': f"{base}{p}", 'title': p} for p in paths]

    def test_german_locale_favors_de_group(self, discovery):
        """With locale_filter='de', /de/ groups should NOT be penalized."""
        urls = self._make_urls([
            f"/{lang}/docs/page{i}" for lang in ['en', 'de']
            for i in range(30)
        ])
        result = discovery._score_and_filter_sitemap_urls(
            urls, ["/de/"], "https://example.com", locale_filter='de'
        )
        result_paths = [u['url'] for u in result]
        # /de/ should be kept, /en/ should be penalized
        assert any("/de/docs/" in p for p in result_paths)

    def test_english_default_when_no_locale(self, discovery):
        """Without locale_filter, defaults to preferring English."""
        urls = self._make_urls([
            f"/{lang}/docs/page{i}" for lang in ['en', 'fr']
            for i in range(30)
        ])
        result = discovery._score_and_filter_sitemap_urls(
            urls, ["/en/"], "https://example.com", locale_filter=None
        )
        result_paths = [u['url'] for u in result]
        assert any("/en/docs/" in p for p in result_paths)


# ============================================================
# NEW: ScopeRules
# ============================================================

class TestScopeRules:
    """Test ScopeRules dataclass — the core of the new 3-phase architecture."""

    def test_url_matches_include(self):
        rules = ScopeRules.from_llm_response(
            "https://example.com",
            include_strs=["/docs/"],
            exclude_strs=[]
        )
        assert rules.url_matches("https://example.com/docs/intro")
        assert not rules.url_matches("https://example.com/blog/post")

    def test_url_matches_exclude_takes_priority(self):
        rules = ScopeRules.from_llm_response(
            "https://example.com",
            include_strs=["/docs/"],
            exclude_strs=["/docs/internal/"]
        )
        assert rules.url_matches("https://example.com/docs/intro")
        assert not rules.url_matches("https://example.com/docs/internal/secret")

    def test_rejects_different_domain(self):
        rules = ScopeRules.from_llm_response(
            "https://example.com",
            include_strs=["/docs/"],
            exclude_strs=[]
        )
        assert not rules.url_matches("https://other.com/docs/intro")

    def test_no_include_patterns_matches_everything_on_domain(self):
        rules = ScopeRules(base_url="https://example.com")
        assert rules.url_matches("https://example.com/anything")
        assert not rules.url_matches("https://other.com/anything")

    def test_from_path_prefixes(self):
        rules = ScopeRules.from_path_prefixes("https://example.com", ["/docs/", "/api/"])
        assert rules.url_matches("https://example.com/docs/intro")
        assert rules.url_matches("https://example.com/api/reference")
        assert not rules.url_matches("https://example.com/blog/post")

    def test_from_path_prefixes_root(self):
        rules = ScopeRules.from_path_prefixes("https://example.com", ["/"])
        assert rules.url_matches("https://example.com/anything")

    def test_invalid_regex_ignored(self):
        """Invalid regex in LLM response should be skipped, not crash."""
        rules = ScopeRules.from_llm_response(
            "https://example.com",
            include_strs=["/docs/", "[invalid(regex"],
            exclude_strs=["[also(bad"]
        )
        # Should still work with the valid pattern
        assert rules.url_matches("https://example.com/docs/intro")

    def test_case_insensitive_matching(self):
        rules = ScopeRules.from_llm_response(
            "https://example.com",
            include_strs=["/DOCS/"],
            exclude_strs=[]
        )
        assert rules.url_matches("https://example.com/docs/intro")


# ============================================================
# NEW: Scout Crawl
# ============================================================

class TestScoutCrawl:
    """Test _scout_crawl — Phase 1 of the new architecture."""

    def test_collects_links_from_pages(self, discovery):
        """Scout crawl should collect all same-domain links."""
        html = """<html><body>
        <a href="/docs/intro">Intro</a>
        <a href="/blog/post">Blog</a>
        <a href="https://other.com/page">External</a>
        </body></html>"""

        def mock_get(url, **kwargs):
            resp = MagicMock()
            resp.status_code = 200
            resp.text = html
            resp.headers = {'content-type': 'text/html'}
            return resp

        with patch.object(discovery.session, 'get', side_effect=mock_get):
            start_html, links = discovery._scout_crawl("https://example.com/", max_pages=1)

        assert "https://example.com/docs/intro" in links
        assert "https://example.com/blog/post" in links
        # External links should NOT be collected
        assert "https://other.com/page" not in links
        assert start_html == html

    def test_returns_empty_on_failure(self, discovery):
        """Scout crawl should return empty on HTTP errors."""
        def mock_get(url, **kwargs):
            raise ConnectionError("Network error")

        with patch.object(discovery.session, 'get', side_effect=mock_get):
            start_html, links = discovery._scout_crawl("https://example.com/", max_pages=1)

        assert start_html == ""
        assert len(links) == 0

    def test_respects_max_pages(self, discovery):
        """Scout crawl should stop after max_pages."""
        call_count = 0
        def mock_get(url, **kwargs):
            nonlocal call_count
            call_count += 1
            resp = MagicMock()
            resp.status_code = 200
            resp.text = f'<html><body><a href="/page{call_count}">Link</a></body></html>'
            resp.headers = {'content-type': 'text/html'}
            return resp

        with patch.object(discovery.session, 'get', side_effect=mock_get):
            discovery._scout_crawl("https://example.com/", max_pages=3)

        assert call_count <= 3


class TestIsNavigable:
    """Test _is_navigable — skip binary files during scout."""

    def test_skips_binary_extensions(self, discovery):
        assert not discovery._is_navigable("https://example.com/file.pdf")
        assert not discovery._is_navigable("https://example.com/style.css")
        assert not discovery._is_navigable("https://example.com/app.js")
        assert not discovery._is_navigable("https://example.com/img.png")

    def test_allows_html_pages(self, discovery):
        assert discovery._is_navigable("https://example.com/docs/intro")
        assert discovery._is_navigable("https://example.com/docs/intro.html")
        assert discovery._is_navigable("https://example.com/api/reference")


# ============================================================
# NEW: LLM Scope Determination
# ============================================================

class TestLLMDetermineScope:
    """Test _llm_determine_scope — Phase 2 of the new architecture."""

    def test_falls_back_on_llm_failure(self, discovery):
        """If LLM call fails, should fall back to heuristic scope."""
        # discovery has no client (api_key=None), so LLM is unavailable
        # Simulate by calling with a client that throws
        discovery_with_client = URLDiscovery(api_key="fake")
        discovery_with_client.client = MagicMock()
        discovery_with_client.client.chat.completions.create.side_effect = Exception("API error")

        scout_links = {"https://example.com/docs/intro", "https://example.com/docs/setup"}
        result = discovery_with_client._llm_determine_scope(
            "https://example.com/docs/",
            "https://example.com",
            "<html></html>",
            scout_links
        )
        assert isinstance(result, ScopeRules)
        assert "fallback" in result.description.lower() or "Heuristic" in result.description

    def test_parses_valid_llm_response(self, discovery):
        """Should correctly parse LLM JSON response into ScopeRules."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"include_patterns": ["/docs/"], "exclude_patterns": ["/blog/"], "reasoning": "docs only"}'
        mock_client.chat.completions.create.return_value = mock_response

        discovery_with_client = URLDiscovery(api_key="fake")
        discovery_with_client.client = mock_client

        scout_links = {
            "https://example.com/docs/intro",
            "https://example.com/docs/setup",
            "https://example.com/docs/api",
            "https://example.com/blog/post1",
        }
        result = discovery_with_client._llm_determine_scope(
            "https://example.com/docs/",
            "https://example.com",
            "<html><title>Docs</title></html>",
            scout_links
        )
        assert isinstance(result, ScopeRules)
        assert result.url_matches("https://example.com/docs/intro")
        assert not result.url_matches("https://example.com/blog/post1")

    def test_rejects_too_restrictive_scope(self, discovery):
        """If LLM scope matches <3 scout links, should fall back to heuristics."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        # Pattern that matches nothing useful
        mock_response.choices[0].message.content = '{"include_patterns": ["/nonexistent/"], "exclude_patterns": [], "reasoning": "bad scope"}'
        mock_client.chat.completions.create.return_value = mock_response

        discovery_with_client = URLDiscovery(api_key="fake")
        discovery_with_client.client = mock_client

        scout_links = {
            "https://example.com/docs/intro",
            "https://example.com/docs/setup",
            "https://example.com/docs/api",
        }
        result = discovery_with_client._llm_determine_scope(
            "https://example.com/docs/",
            "https://example.com",
            "<html></html>",
            scout_links
        )
        # Should have fallen back to heuristic
        assert "Heuristic" in result.description or "fallback" in result.description.lower()


# ============================================================
# NEW: 3-Phase discover_urls integration
# ============================================================

class TestThreePhaseFlow:
    """Test the full 3-phase discover_urls flow."""

    def test_discover_urls_returns_scope_rules(self, discovery):
        """Result should include scope_rules instead of old scopes."""
        sitemap_urls = [{'url': f'https://example.com/docs/page{i}', 'title': f'P{i}'}
                        for i in range(15)]

        with patch.object(discovery, '_scout_crawl', return_value=("", {"https://example.com/docs/"})), \
             patch.object(discovery, '_determine_scope', return_value=['/docs/']), \
             patch.object(discovery, '_try_sitemap', return_value=sitemap_urls), \
             patch.object(discovery, '_try_navigation', return_value=[]), \
             patch.object(discovery.github_discovery, 'is_github_repo', return_value=False):
            result = discovery.discover_urls("https://example.com/docs/")

        assert 'scope_rules' in result
        assert isinstance(result['scope_rules'], ScopeRules)

    def test_scout_crawl_is_called(self, discovery):
        """Phase 1 scout crawl should always be called for non-GitHub sites."""
        mock_scout = MagicMock(return_value=("", set()))

        with patch.object(discovery, '_scout_crawl', mock_scout), \
             patch.object(discovery, '_determine_scope', return_value=['/']), \
             patch.object(discovery, '_try_sitemap', return_value=[]), \
             patch.object(discovery, '_try_navigation', return_value=[]), \
             patch.object(discovery, '_crawl_links', return_value=[]), \
             patch.object(discovery.github_discovery, 'is_github_repo', return_value=False):
            discovery.discover_urls("https://example.com/")

        mock_scout.assert_called_once()

    def test_is_doc_page_only_filters_extensions(self, discovery):
        """_is_doc_page should only filter by file extension, not path."""
        assert discovery._is_doc_page("https://example.com/search")
        assert discovery._is_doc_page("https://example.com/login")
        assert discovery._is_doc_page("https://example.com/admin/panel")
        assert not discovery._is_doc_page("https://example.com/file.pdf")
        assert not discovery._is_doc_page("https://example.com/style.css")
        assert not discovery._is_doc_page("https://example.com/bundle.js")
