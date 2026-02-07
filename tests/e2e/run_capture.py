"""Capture HTML from reference doc-sets for offline E2E testing."""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))
from response_capture import ResponseCapture
from url_discovery import URLDiscovery

MANIFEST = Path(__file__).parent.parent / "fixtures" / "real-world" / "capture-manifest.json"
FIXTURES = Path(__file__).parent.parent / "fixtures" / "real-world"


def discover_and_capture(doc_name: str, start_url: str, max_pages: int, capture: ResponseCapture) -> dict:
    """Run URL discovery and capture all discovered pages."""
    print(f"\n=== {doc_name}: Discovering URLs ===")
    
    discovery = URLDiscovery()
    discovered = discovery.discover_urls(start_url, max_pages=max_pages)
    
    urls = [u['url'] for u in discovered['urls']]
    print(f"  Discovered {len(urls)} URLs (mode: {discovered['mode']})")
    
    if not urls:
        return {"ok": 0, "fail": 0, "urls": []}
    
    print(f"\n=== {doc_name}: Capturing {len(urls)} pages ===")
    results = {"ok": 0, "fail": 0, "urls": []}
    
    for url in urls:
        try:
            resp = capture.capture(url, timeout=15)
            meta_path, body_path = capture.save(resp, doc_name)
            body_kb = len(resp.body) / 1024
            print(f"  OK  {url[:60]}... -> {body_path.name} ({body_kb:.0f} KB)")
            results["ok"] += 1
            results["urls"].append({
                "url": url,
                "captured_at": datetime.now().isoformat(),
                "size_bytes": len(resp.body)
            })
        except Exception as e:
            print(f"  FAIL {url[:60]}...: {e}")
            results["fail"] += 1
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Capture HTML from doc sites")
    parser.add_argument("--max-pages-per-site", type=int, default=50,
                        help="Max pages to capture per site (default: 50)")
    parser.add_argument("--sites", nargs="+", default=None,
                        help="Specific sites to capture (default: all 10)")
    parser.add_argument("--list", action="store_true",
                        help="List available sites and exit")
    args = parser.parse_args()
    
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    
    if args.list:
        print("Available sites:")
        for doc_set in manifest["doc_sets"]:
            print(f"  - {doc_set['doc_name']}")
        return
    
    # Determine which sites to capture
    target_sites = args.sites if args.sites else [d["doc_name"] for d in manifest["doc_sets"]]
    
    capture = ResponseCapture(fixtures_dir=str(FIXTURES))
    all_results = {}
    
    for doc_set in manifest["doc_sets"]:
        name = doc_set["doc_name"]
        if name not in target_sites:
            continue
        
        start_url = doc_set["urls"][0]["url"] if doc_set["urls"] else None
        if not start_url:
            print(f"Warning: No start URL for {name}")
            continue
        
        results = discover_and_capture(name, start_url, args.max_pages_per_site, capture)
        all_results[name] = results
    
    # Update manifest with capture info
    update_capture_manifest(manifest, all_results)
    
    # Print summary
    print("\n" + "="*50)
    print("CAPTURE SUMMARY")
    print("="*50)
    total_ok = total_fail = 0
    for name, r in all_results.items():
        print(f"  {name:12}: {r['ok']:3} captured, {r['fail']:2} failed")
        total_ok += r["ok"]
        total_fail += r["fail"]
    print("-"*50)
    print(f"  {'TOTAL':12}: {total_ok:3} captured, {total_fail:2} failed")
    print(f"\nCaptured at: {datetime.now().isoformat()}")


def update_capture_manifest(manifest: dict, results: dict):
    """Update manifest with capture timestamps and counts."""
    manifest["last_capture_run"] = datetime.now().isoformat()
    
    for doc_set in manifest["doc_sets"]:
        name = doc_set["doc_name"]
        if name in results:
            doc_set["capture_info"] = {
                "captured_at": datetime.now().isoformat(),
                "pages_captured": results[name]["ok"],
                "pages_failed": results[name]["fail"]
            }
    
    # Save updated manifest
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
