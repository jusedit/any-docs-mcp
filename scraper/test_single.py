#!/usr/bin/env python3
"""Test a single site from the batch list."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from batch_test_50 import run_site

if __name__ == "__main__":
    name = sys.argv[1]
    url = sys.argv[2]
    max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
    result = run_site(name, url, max_pages=max_pages)
    print(f"\n{'='*60}")
    print(f"RESULT: {result}")
    print(f"{'='*60}")
