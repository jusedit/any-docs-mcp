"""pytest configuration and fixtures for scraper tests."""
import pytest
from pathlib import Path
from storage import StorageManager


@pytest.fixture
def tmp_storage(tmp_path):
    """Create a temporary StorageManager for testing.
    
    Returns:
        StorageManager: A StorageManager rooted in a temp directory.
    """
    return StorageManager(str(tmp_path))
