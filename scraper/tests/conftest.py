"""pytest configuration and fixtures for scraper tests."""
import pytest
from pathlib import Path
from storage import StorageManager
from scraper.tests.fixture_server import FixtureHTTPServer


@pytest.fixture
def tmp_storage(tmp_path):
    """Create a temporary StorageManager for testing.
    
    Returns:
        StorageManager: A StorageManager rooted in a temp directory.
    """
    return StorageManager(str(tmp_path))


@pytest.fixture(scope="function")
def mock_http_server(tmp_path):
    """Pytest fixture that yields a started FixtureHTTPServer.
    
    Usage:
        def test_something(mock_http_server):
            url = mock_http_server.get_rewritten_url("https://example.com/page")
            response = requests.get(url)
            ...
    """
    # Use temp fixtures dir for isolation
    fixtures_dir = tmp_path / "fixtures"
    
    server = FixtureHTTPServer(fixtures_dir=str(fixtures_dir))
    base_url = server.start()
    
    yield server
    
    server.stop()


@pytest.fixture(scope="session")
def real_world_fixtures_dir():
    """Returns the path to real-world fixtures directory."""
    # Path relative to project root
    return Path(__file__).parent.parent.parent / "tests" / "fixtures" / "real-world"
