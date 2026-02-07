"""Runner script to capture all URLs from the manifest."""
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

from response_capture import ResponseCapture


def load_manifest(manifest_path: str = None) -> Dict[str, Any]:
    """Load the capture manifest from JSON."""
    if manifest_path is None:
        # Default: look in project root's tests/fixtures
        project_root = Path(__file__).parent.parent
        manifest_path = project_root / "tests" / "fixtures" / "real-world" / "capture-manifest.json"
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def capture_all(doc_sets: List[str] = None, manifest_path: str = None, fixtures_dir: str = None) -> Dict[str, Any]:
    """Capture all URLs from the manifest.
    
    Args:
        doc_sets: Optional list of doc_names to capture. If None, captures all.
        manifest_path: Path to capture-manifest.json
        fixtures_dir: Directory to store captured fixtures
        
    Returns:
        Report dict with captured_count, errors, total_urls
    """
    if manifest_path is None:
        manifest_path = "tests/fixtures/real-world/capture-manifest.json"
    
    manifest = load_manifest(manifest_path)
    capture = ResponseCapture(fixtures_dir=fixtures_dir or "tests/fixtures/real-world")
    
    results = {
        "captured_count": 0,
        "errors": [],
        "total_urls": 0,
        "by_doc_set": {}
    }
    
    for doc_set in manifest["doc_sets"]:
        doc_name = doc_set["doc_name"]
        
        # Skip if specific doc_sets specified and this isn't one
        if doc_sets and doc_name not in doc_sets:
            continue
        
        print(f"\nCapturing {doc_name} ({doc_set['site_type']})...")
        
        doc_results = {
            "captured": 0,
            "errors": []
        }
        
        for url_entry in doc_set["urls"]:
            url = url_entry["url"]
            page_type = url_entry.get("page_type", "unknown")
            results["total_urls"] += 1
            
            print(f"  [{page_type}] {url}")
            
            try:
                resp = capture.capture(url)
                meta_path, body_path = capture.save(resp, doc_name)
                print(f"    → {meta_path.name}")
                results["captured_count"] += 1
                doc_results["captured"] += 1
                
            except Exception as e:
                error_msg = f"{doc_name}: {url} - {e}"
                print(f"    ERROR: {e}")
                results["errors"].append(error_msg)
                doc_results["errors"].append(str(e))
        
        results["by_doc_set"][doc_name] = doc_results
    
    return results


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Capture HTTP responses for real-world testing fixtures")
    parser.add_argument("--manifest", "-m", default="tests/fixtures/real-world/capture-manifest.json",
                        help="Path to capture-manifest.json")
    parser.add_argument("--fixtures-dir", "-f", default="tests/fixtures/real-world",
                        help="Directory to store captured fixtures")
    parser.add_argument("--doc-sets", "-d", nargs="+",
                        help="Specific doc-sets to capture (default: all)")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List available doc-sets and exit")
    
    args = parser.parse_args()
    
    if args.list:
        manifest = load_manifest(args.manifest)
        print("Available doc-sets:")
        for doc_set in manifest["doc_sets"]:
            url_count = len(doc_set["urls"])
            print(f"  {doc_set['doc_name']:20} ({doc_set['site_type']:12}) - {url_count} URLs")
        sys.exit(0)
    
    print(f"Loading manifest from: {args.manifest}")
    print(f"Fixtures directory: {args.fixtures_dir}")
    
    if args.doc_sets:
        print(f"Capturing specific doc-sets: {', '.join(args.doc_sets)}")
    else:
        print("Capturing all doc-sets")
    
    results = capture_all(
        doc_sets=args.doc_sets,
        manifest_path=args.manifest,
        fixtures_dir=args.fixtures_dir
    )
    
    print("\n" + "="*60)
    print(f"Capture complete: {results['captured_count']}/{results['total_urls']} URLs captured")
    
    if results['errors']:
        print(f"Errors: {len(results['errors'])}")
        for error in results['errors'][:5]:  # Show first 5
            print(f"  - {error}")
        if len(results['errors']) > 5:
            print(f"  ... and {len(results['errors']) - 5} more")
    
    # Exit with error code if any failures
    sys.exit(0 if results['captured_count'] == results['total_urls'] else 1)


if __name__ == "__main__":
    main()
