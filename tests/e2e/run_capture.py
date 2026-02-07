"""Capture HTML from reference doc-sets for offline E2E testing."""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))
from response_capture import ResponseCapture

MANIFEST = Path(__file__).parent.parent / "fixtures" / "real-world" / "capture-manifest.json"
FIXTURES = Path(__file__).parent.parent / "fixtures" / "real-world"

TARGET_SITES = ["react", "fastapi", "kubernetes"]


def main():
    capture = ResponseCapture(fixtures_dir=str(FIXTURES))

    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)

    results = {}
    for doc_set in manifest["doc_sets"]:
        name = doc_set["doc_name"]
        if name not in TARGET_SITES:
            continue

        urls = doc_set["urls"]
        results[name] = {"ok": 0, "fail": 0}
        print(f"\n=== Capturing {name} ({len(urls)} URLs) ===")

        for entry in urls:
            url = entry["url"]
            try:
                resp = capture.capture(url, timeout=15)
                meta_path, body_path = capture.save(resp, name)
                body_kb = len(resp.body) / 1024
                print(f"  OK  {url} -> {body_path.name} ({body_kb:.0f} KB)")
                results[name]["ok"] += 1
            except Exception as e:
                print(f"  FAIL {url}: {e}")
                results[name]["fail"] += 1

    print("\n=== Summary ===")
    total_ok = 0
    for name, r in results.items():
        print(f"  {name}: {r['ok']} captured, {r['fail']} failed")
        total_ok += r["ok"]
    print(f"  Total: {total_ok} files captured")


if __name__ == "__main__":
    main()
