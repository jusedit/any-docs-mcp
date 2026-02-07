"""Smoke test for scraper module imports - verifies all modules load correctly."""


def test_import_content_cleaner():
    """ContentCleaner imports successfully."""
    from content_cleaner import ContentCleaner
    assert ContentCleaner is not None


def test_import_scraper_engine():
    """ScraperEngine imports successfully."""
    from scraper_engine import ScraperEngine
    assert ScraperEngine is not None


def test_import_storage_manager():
    """StorageManager imports successfully."""
    from storage import StorageManager
    assert StorageManager is not None


def test_import_url_discovery():
    """URLDiscovery imports successfully."""
    from url_discovery import URLDiscovery
    assert URLDiscovery is not None


def test_import_github_discovery():
    """GitHubDiscovery imports successfully."""
    from github_discovery import GitHubDiscovery
    assert GitHubDiscovery is not None


def test_import_sitemap_parser():
    """SitemapParser imports successfully."""
    from sitemap_parser import SitemapParser
    assert SitemapParser is not None


def test_import_site_analysis():
    """SiteAnalysis model imports successfully."""
    from models import SiteAnalysis
    assert SiteAnalysis is not None
