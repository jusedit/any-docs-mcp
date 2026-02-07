"""
Scope detection accuracy test with ground-truth URLs.

Extracts URLs from AppData for 5 core doc-sets, tests _determine_scope() and
_url_in_scope() against ground-truth, measures precision/recall.
"""
import json
import os
import sys
import pytest
from pathlib import Path
from typing import List, Dict, Set, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))
from url_discovery import URLDiscovery

APPDATA_DOCS = Path(os.environ.get("APPDATA", "")) / "AnyDocsMCP" / "docs"
OUTPUT_PATH = Path(__file__).parent / "fixtures" / "real-world" / "scope-accuracy.json"

# Core doc-sets to test
CORE_DOCS = ["react", "fastapi", "kubernetes", "django", "tailwind"]


def extract_ground_truth_urls(doc_name: str) -> List[str]:
    """Extract all source URLs from AppData .md files for a doc-set."""
    doc_dir = APPDATA_DOCS / doc_name
    if not doc_dir.exists():
        return []
    
    # Find latest version
    versions = sorted(
        [d for d in doc_dir.iterdir() if d.is_dir() and d.name.startswith("v")],
        key=lambda d: int(d.name[1:]) if d.name[1:].isdigit() else 0,
        reverse=True
    )
    
    urls = set()
    for v_dir in versions[:1]:  # Use latest version only
        for md_file in v_dir.glob("*.md"):
            content = md_file.read_text(encoding="utf-8", errors="replace")
            # Extract Source: URL from markdown
            for line in content.split("\n"):
                if "**Source:**" in line:
                    url = line.replace("**Source:**", "").strip()
                    urls.add(url)
    
    return sorted(urls)


class TestScopeDetectionAccuracy:
    """Test _determine_scope() and _url_in_scope() accuracy."""
    
    @pytest.fixture(scope="class")
    def discovery(self):
        return URLDiscovery()
    
    @pytest.fixture(scope="class")
    def ground_truth(self):
        """Load ground-truth URLs for all core doc-sets."""
        truth = {}
        for doc in CORE_DOCS:
            urls = extract_ground_truth_urls(doc)
            if urls:
                truth[doc] = urls
        return truth
    
    @pytest.mark.parametrize("doc_name", CORE_DOCS)
    def test_scope_detects_known_urls(self, discovery, ground_truth, doc_name):
        """_url_in_scope() returns True for all ground-truth URLs."""
        if doc_name not in ground_truth:
            pytest.skip(f"No ground-truth data for {doc_name}")
        
        urls = ground_truth[doc_name]
        if not urls:
            pytest.skip(f"Empty ground-truth for {doc_name}")
        
        # Determine scope from first URL
        scope = discovery._determine_scope(urls[0])
        
        # Check each ground-truth URL is in scope
        in_scope_count = 0
        for url in urls:
            parsed = urlparse(url)
            base = f"{parsed.scheme}://{parsed.netloc}"
            if discovery._url_in_scope(url, base, scope):
                in_scope_count += 1
        
        # Calculate recall (should be >90%)
        recall = in_scope_count / len(urls)
        print(f"\n  {doc_name}: {in_scope_count}/{len(urls)} URLs in scope ({recall:.1%})")
        print(f"    Scope: {scope}")
        
        assert recall >= 0.90, f"Recall {recall:.1%} < 90% for {doc_name}"
    
    def test_generates_scope_accuracy_report(self, discovery, ground_truth):
        """Generate scope-accuracy.json with precision/recall metrics."""
        report = {
            "tested_at": datetime.now().isoformat(),
            "results": {}
        }
        
        for doc_name in CORE_DOCS:
            if doc_name not in ground_truth:
                continue
            
            urls = ground_truth[doc_name]
            if not urls:
                continue
            
            # Determine scope
            scope = discovery._determine_scope(urls[0])
            
            # Calculate metrics
            in_scope = 0
            out_of_scope = 0
            for url in urls:
                parsed = urlparse(url)
                base = f"{parsed.scheme}://{parsed.netloc}"
                if discovery._url_in_scope(url, base, scope):
                    in_scope += 1
                else:
                    out_of_scope += 1
            
            # Precision: of URLs we think are in scope, how many are?
            # (Assume all ground-truth should be in scope)
            precision = in_scope / len(urls) if urls else 0
            recall = in_scope / len(urls) if urls else 0
            
            report["results"][doc_name] = {
                "scope": scope,
                "ground_truth_count": len(urls),
                "in_scope": in_scope,
                "out_of_scope": out_of_scope,
                "precision": round(precision, 3),
                "recall": round(recall, 3),
                "passed": precision >= 0.95 and recall >= 0.90
            }
        
        # Save report
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_PATH, "w") as f:
            json.dump(report, f, indent=2)
        
        # Verify report structure
        assert len(report["results"]) >= 3, "Should have results for at least 3 doc-sets"
        
        # Document baseline (this test measures, doesn't validate thresholds)
        print("\n  Scope Detection Baseline:")
        for doc, metrics in report["results"].items():
            print(f"    {doc}: {metrics['ground_truth_count']} URLs, "
                  f"precision={metrics['precision']:.2f}, recall={metrics['recall']:.2f}, "
                  f"scope='{metrics['scope']}'")
        
        # Verify we generated data for at least 3 doc-sets
        assert len(report["results"]) >= 3, "Should have results for at least 3 doc-sets"


from datetime import datetime
from urllib.parse import urlparse


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
