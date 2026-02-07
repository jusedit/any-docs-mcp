"""
Fix query-suite.json by matching expected_top_title to REAL headings in AppData.

For each query, searches the actual .md files for the closest matching h2 heading
and updates expected_top_title + expected_file accordingly.
"""
import json
import os
import re
from pathlib import Path
from difflib import SequenceMatcher

APPDATA_DOCS = Path(os.environ["APPDATA"]) / "AnyDocsMCP" / "docs"
QUERY_SUITE = Path(__file__).parent.parent / "fixtures" / "real-world" / "query-suite.json"

VERSIONS = {
    "react": "v2", "fastapi": "v2", "tailwind": "v4", "kubernetes": "v2",
    "django": "v1", "hyperapp-github": "v2", "onoffice": "v18",
    "synthflow": "v2", "golang": "v1", "rust-book": "v2",
}

def clean_heading(h: str) -> str:
    """Remove permalink artifacts from heading text."""
    h = re.sub(r'\[?\u00b6\]?\(#[^)]*(?:\s*"[^"]*")?\)', '', h)
    h = re.sub(r'\[?\u00b6\]?', '', h)
    h = re.sub(r'\[([^\]]*)\]\(#[^)]*\)', r'\1', h)  # [text](#anchor) -> text
    h = re.sub(r'\[]\(#[^)]*\)', '', h)  # [](#anchor) -> empty
    return h.strip()

def build_heading_index(doc_name: str) -> list:
    """Build index of all h2 headings per file for a doc-set."""
    ver = VERSIONS.get(doc_name)
    if not ver:
        return []
    
    docs_path = APPDATA_DOCS / doc_name / ver
    if not docs_path.exists():
        return []
    
    headings = []
    for md_file in docs_path.glob("*.md"):
        content = md_file.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r'^##\s+(.+)$', content, re.MULTILINE):
            title = clean_heading(match.group(1))
            if title and len(title) > 2:
                headings.append({
                    "file": md_file.stem,
                    "title": title,
                })
    return headings

def find_best_match(query_title: str, headings: list) -> tuple:
    """Find the best matching heading for a query's expected title."""
    query_lower = query_title.lower()
    best_score = 0
    best_match = None
    
    for h in headings:
        title_lower = h["title"].lower()
        
        # Exact match
        if title_lower == query_lower:
            return h["title"], h["file"], 1.0
        
        # Contains match
        if query_lower in title_lower or title_lower in query_lower:
            score = 0.8
            if score > best_score:
                best_score = score
                best_match = h
        
        # Fuzzy match
        ratio = SequenceMatcher(None, query_lower, title_lower).ratio()
        if ratio > best_score:
            best_score = ratio
            best_match = h
    
    if best_match and best_score >= 0.4:
        return best_match["title"], best_match["file"], best_score
    return None, None, 0

def main():
    with open(QUERY_SUITE) as f:
        suite = json.load(f)
    
    queries = suite["queries"]
    fixed = 0
    not_found = 0
    
    # Pre-build heading indices
    heading_indices = {}
    for doc in VERSIONS:
        heading_indices[doc] = build_heading_index(doc)
    
    for q in queries:
        doc_name = q["doc_name"]
        headings = heading_indices.get(doc_name, [])
        
        if not headings:
            not_found += 1
            continue
        
        title, file, score = find_best_match(q["expected_top_title"], headings)
        
        if title:
            old_title = q["expected_top_title"]
            old_file = q["expected_file"]
            q["expected_top_title"] = title
            q["expected_file"] = file + ".md"
            if old_title != title or old_file != q["expected_file"]:
                fixed += 1
                print(f"  [{doc_name}] '{old_title}' -> '{title}' (file: {file}, score: {score:.2f})")
        else:
            not_found += 1
            print(f"  [{doc_name}] NO MATCH for '{q['expected_top_title']}' (query: '{q['query']}')")
    
    # Write updated suite
    with open(QUERY_SUITE, "w", encoding="utf-8") as f:
        json.dump(suite, f, indent=2, ensure_ascii=False)
    
    print(f"\nDone: {fixed} fixed, {not_found} not found, {len(queries)} total")

if __name__ == "__main__":
    main()
