"""Capture HTML from reference doc-sets for offline E2E testing."""
import argparse
import json
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))
from response_capture import ResponseCapture
from url_discovery import URLDiscovery

MANIFEST = Path(__file__).parent.parent / "fixtures" / "real-world" / "capture-manifest.json"
FIXTURES = Path(__file__).parent.parent / "fixtures" / "real-world"


def check_freshness(doc_name: str, fixtures_dir: Path, max_age_days: int = 90) -> dict:
    """Check freshness of captured files for a doc-set.
    
    Returns:
        dict with fresh_count, stale_count, total_count, stale_files list
    """
    doc_dir = fixtures_dir / doc_name
    if not doc_dir.exists():
        return {"fresh": 0, "stale": 0, "total": 0, "stale_files": []}
    
    now = datetime.now()
    max_age = timedelta(days=max_age_days)
    
    fresh = stale = 0
    stale_files = []
    
    for meta_file in doc_dir.glob("*.meta.json"):
        try:
            with open(meta_file, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            
            captured_at = meta.get("captured_at")
            if captured_at:
                captured_date = datetime.fromisoformat(captured_at.replace('Z', '+00:00').replace('+00:00', ''))
                age = now - captured_date
                
                if age > max_age:
                    stale += 1
                    stale_files.append(meta_file.stem.replace('.meta', ''))
                else:
                    fresh += 1
            else:
                # No timestamp = stale
                stale += 1
                stale_files.append(meta_file.stem.replace('.meta', ''))
        except Exception:
            stale += 1
            stale_files.append(meta_file.stem.replace('.meta', ''))
    
    return {
        "fresh": fresh,
        "stale": stale,
        "total": fresh + stale,
        "stale_files": stale_files
    }


def backup_existing_capture(doc_dir: Path, slug: str):
    """Backup existing capture files before overwriting."""
    # Backup body files (both .html and .html.gz)
    for ext in ['.body.html', '.body.html.gz']:
        body_path = doc_dir / f"{slug}{ext}"
        if body_path.exists():
            backup_path = doc_dir / f"{slug}{ext}.bak"
            shutil.copy2(body_path, backup_path)
    
    # Backup meta
    meta_path = doc_dir / f"{slug}.meta.json"
    if meta_path.exists():
        backup_path = doc_dir / f"{slug}.meta.json.bak"
        shutil.copy2(meta_path, backup_path)


def discover_and_capture(doc_name: str, start_url: str, max_pages: int, capture: ResponseCapture, 
                         fixtures_dir: Path, refresh_mode: bool = False, max_age_days: int = 90) -> dict:
    """Run URL discovery and capture all discovered pages."""
    print(f"\n=== {doc_name}: Discovering URLs ===")
    
    discovery = URLDiscovery()
    discovered = discovery.discover_urls(start_url, max_pages=max_pages)
    
    urls = [u['url'] for u in discovered['urls']]
    print(f"  Discovered {len(urls)} URLs (mode: {discovered['mode']})")
    
    if not urls:
        return {"ok": 0, "fail": 0, "urls": [], "skipped": 0}
    
    # Check freshness if in refresh mode
    if refresh_mode:
        freshness = check_freshness(doc_name, fixtures_dir, max_age_days)
        print(f"  Freshness check: {freshness['fresh']} fresh, {freshness['stale']} stale (>{max_age_days} days)")
        stale_slugs = set(freshness["stale_files"])
    else:
        stale_slugs = None
    
    print(f"\n=== {doc_name}: Capturing {len(urls)} pages ===")
    results = {"ok": 0, "fail": 0, "skipped": 0, "urls": []}
    
    for url in urls:
        # In refresh mode, skip fresh pages
        if refresh_mode and stale_slugs is not None:
            from response_capture import ResponseCapture as RC
            slug = RC.url_to_slug(url)
            if slug not in stale_slugs:
                print(f"  SKIP {url[:60]}... (fresh)")
                results["skipped"] += 1
                continue
        
        # Backup existing if in refresh mode
        if refresh_mode:
            doc_dir = fixtures_dir / doc_name
            from response_capture import ResponseCapture as RC
            slug = RC.url_to_slug(url)
            backup_existing_capture(doc_dir, slug)
        
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
    parser.add_argument("--refresh", action="store_true",
                        help="Only re-capture stale pages (older than --max-age-days)")
    parser.add_argument("--max-age-days", type=int, default=90,
                        help="Max age in days before a capture is considered stale (default: 90)")
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
        
        results = discover_and_capture(name, start_url, args.max_pages_per_site, capture, 
                                         FIXTURES, args.refresh, args.max_age_days)
        all_results[name] = results
    
    # Update manifest with capture info
    update_capture_manifest(manifest, all_results)
    
    # Print summary with freshness info
    print("\n" + "="*50)
    print("CAPTURE SUMMARY")
    print("="*50)
    
    # Calculate freshness stats
    total_fresh = total_stale = total_captured = 0
    for name, r in all_results.items():
        freshness = check_freshness(name, FIXTURES, args.max_age_days)
        total_fresh += freshness["fresh"]
        total_stale += freshness["stale"]
        total_captured += freshness["total"]
        
        skip_info = f", {r.get('skipped', 0)} skipped" if args.refresh else ""
        print(f"  {name:12}: {r['ok']:3} captured, {r['fail']:2} failed{skip_info}")
    
    print("-"*50)
    total_ok = sum(r["ok"] for r in all_results.values())
    total_fail = sum(r["fail"] for r in all_results.values())
    total_skipped = sum(r.get("skipped", 0) for r in all_results.values())
    
    if args.refresh:
        print(f"  {'TOTAL':12}: {total_ok:3} captured, {total_fail:2} failed, {total_skipped:3} skipped")
        print(f"  {'FRESHNESS':12}: {total_fresh} fresh, {total_stale} stale (> {args.max_age_days} days)")
    else:
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
