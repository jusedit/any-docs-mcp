"""Compare old vs new scraped versions for quality improvements."""
import os
import re
import sys
from pathlib import Path
from collections import defaultdict

DOCS_ROOT = Path(os.environ.get("APPDATA", "")) / "AnyDocsMCP" / "docs"

SITES = {
    "react": ("v2", "v3"),
    "fastapi": ("v2", "v4"),
    "tailwind": ("v4", "v5"),
    "kubernetes": ("v2", "v3"),
    "django": ("v2", "v3"),
}

# Quality checks
def count_html_residue(content: str) -> int:
    patterns = [r'<div[ >]', r'<span[ >]', r'<script', r'<style', r'<nav[ >]', r'<footer', r'<header']
    return sum(len(re.findall(p, content, re.IGNORECASE)) for p in patterns)

def count_encoding_errors(content: str) -> int:
    patterns = [r'â€™', r'â€"', r'â€œ', r'â€\x9d', r'Ã¤', r'Ã¶', r'Ã¼', r'Ã©', r'â€˜', r'Â»', r'Â«', r'\ufffd']
    return sum(len(re.findall(p, content)) for p in patterns)

def count_ui_artifacts(content: str) -> int:
    patterns = [
        r'Copy to clipboard', r'Copied!', r'Show more', r'Show less',
        r'On this page', r'Table of Contents', r'Edit this page',
        r'Was this page helpful', r'Cookie', r'cookie',
        r'PreviousNext', r'Back to top',
    ]
    return sum(len(re.findall(p, content, re.IGNORECASE)) for p in patterns)

BAD_LABELS = {'shiki', 'highlight', 'code-block', 'language-undefined', 'sp-pre-placeholder', 'index-module__doxijg__content'}

def count_code_blocks(content: str) -> dict:
    blocks = re.findall(r'```(\w*)', content)
    labeled = sum(1 for b in blocks if b and b.lower() not in BAD_LABELS)
    unlabeled = sum(1 for b in blocks if not b or b.lower() in BAD_LABELS)
    return {"labeled": labeled, "unlabeled": unlabeled}

def count_headings(content: str) -> dict:
    headings = re.findall(r'^(#{1,6})\s', content, re.MULTILINE)
    return {"total": len(headings), "h1": headings.count("#"), "h2": headings.count("##")}

def analyze_version(site: str, version: str) -> dict:
    version_dir = DOCS_ROOT / site / version
    if not version_dir.exists():
        return {"error": f"{version_dir} not found"}
    
    md_files = list(version_dir.glob("*.md"))
    if not md_files:
        return {"files": 0, "error": "no .md files"}
    
    totals = defaultdict(int)
    totals["files"] = len(md_files)
    totals["total_size_kb"] = 0
    code_totals = {"labeled": 0, "unlabeled": 0}
    heading_totals = {"total": 0, "h1": 0, "h2": 0}
    
    for f in md_files:
        content = f.read_text(encoding="utf-8", errors="replace")
        totals["total_size_kb"] += len(content.encode("utf-8")) / 1024
        totals["html_residue"] += count_html_residue(content)
        totals["encoding_errors"] += count_encoding_errors(content)
        totals["ui_artifacts"] += count_ui_artifacts(content)
        
        cb = count_code_blocks(content)
        code_totals["labeled"] += cb["labeled"]
        code_totals["unlabeled"] += cb["unlabeled"]
        
        hd = count_headings(content)
        heading_totals["total"] += hd["total"]
        heading_totals["h1"] += hd["h1"]
        heading_totals["h2"] += hd["h2"]
    
    totals["total_size_kb"] = round(totals["total_size_kb"], 1)
    totals["code_blocks_labeled"] = code_totals["labeled"]
    totals["code_blocks_unlabeled"] = code_totals["unlabeled"]
    totals["code_label_rate"] = round(
        code_totals["labeled"] / max(code_totals["labeled"] + code_totals["unlabeled"], 1) * 100, 1
    )
    totals["headings_total"] = heading_totals["total"]
    totals["headings_h1"] = heading_totals["h1"]
    totals["headings_h2"] = heading_totals["h2"]
    
    return dict(totals)


def main():
    print("=" * 80)
    print("QUALITY COMPARISON: Old Version vs New Version")
    print("=" * 80)
    
    for site, (old_v, new_v) in SITES.items():
        print(f"\n{'─' * 80}")
        print(f"  {site.upper()} ({old_v} → {new_v})")
        print(f"{'─' * 80}")
        
        old = analyze_version(site, old_v)
        new = analyze_version(site, new_v)
        
        if "error" in old:
            print(f"  OLD: {old['error']}")
        if "error" in new:
            print(f"  NEW: {new['error']}")
        if "error" in old or "error" in new:
            continue
        
        metrics = [
            ("Files", "files", False),
            ("Total Size (KB)", "total_size_kb", False),
            ("HTML Residue Tags", "html_residue", True),
            ("Encoding Errors", "encoding_errors", True),
            ("UI Artifacts", "ui_artifacts", True),
            ("Code Blocks (labeled)", "code_blocks_labeled", False),
            ("Code Blocks (unlabeled)", "code_blocks_unlabeled", True),
            ("Code Label Rate (%)", "code_label_rate", False),
            ("Headings Total", "headings_total", False),
        ]
        
        print(f"  {'Metric':<30} {'Old':>10} {'New':>10} {'Delta':>10} {'Result':>8}")
        print(f"  {'─' * 68}")
        
        improvements = 0
        regressions = 0
        
        for label, key, lower_is_better in metrics:
            o = old.get(key, 0)
            n = new.get(key, 0)
            delta = n - o
            
            if lower_is_better:
                result = "✅ BETTER" if delta < 0 else ("⚠️ WORSE" if delta > 0 else "= SAME")
                if delta < 0: improvements += 1
                elif delta > 0: regressions += 1
            else:
                result = "✅ BETTER" if delta > 0 else ("⚠️ WORSE" if delta < 0 else "= SAME")
                if delta > 0: improvements += 1
                elif delta < 0: regressions += 1
            
            delta_str = f"+{delta}" if delta > 0 else str(delta)
            print(f"  {label:<30} {o:>10} {n:>10} {delta_str:>10} {result:>8}")
        
        print(f"\n  Summary: {improvements} improvements, {regressions} regressions")
    
    print(f"\n{'=' * 80}")
    print("DONE")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
