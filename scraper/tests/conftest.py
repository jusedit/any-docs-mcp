"""Shared fixtures for scraper tests."""
import sys
from pathlib import Path

import pytest

# Add scraper to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))
