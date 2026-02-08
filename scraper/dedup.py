"""Cross-page diff deduplication.

Core insight: on a documentation site, content that repeats across multiple
pages is UI residue (nav, header, footer, breadcrumbs). Content that is
unique to each page is the actual documentation.

Algorithm:
1. After initial crawl, read N sample pages (raw markdown)
2. Split each page into "blocks" (separated by blank lines or headings)
3. Count how many pages each block appears in
4. Blocks appearing in >50% of pages are UI residue → remove from all files
5. Re-write cleaned files
"""
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Set, Tuple


MIN_BLOCK_LENGTH = 15
MIN_PAGES_FOR_DEDUP = 3
REPEAT_THRESHOLD = 0.5


def _split_into_blocks(content: str) -> List[str]:
    """Split markdown content into logical blocks.

    A block is a group of non-empty lines separated by blank lines
    or heading boundaries.
    """
    lines = content.split("\n")
    blocks = []
    current: List[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped == "" or stripped.startswith("# "):
            if current:
                block = "\n".join(current).strip()
                if block:
                    blocks.append(block)
                current = []
            if stripped.startswith("# "):
                current.append(line)
        else:
            current.append(line)

    if current:
        block = "\n".join(current).strip()
        if block:
            blocks.append(block)

    return blocks


def _normalize_block(block: str) -> str:
    """Normalize a block for comparison (collapse whitespace, lowercase)."""
    text = re.sub(r"\s+", " ", block).strip().lower()
    return text


def find_repeated_blocks(file_contents: Dict[str, str]) -> Set[str]:
    """Find blocks that repeat across multiple pages.

    Args:
        file_contents: {filepath: markdown_content}

    Returns:
        Set of normalized block strings that appear in >REPEAT_THRESHOLD of pages.
    """
    num_pages = len(file_contents)
    if num_pages < MIN_PAGES_FOR_DEDUP:
        return set()

    block_page_count: Counter = Counter()

    for filepath, content in file_contents.items():
        blocks = _split_into_blocks(content)
        seen_in_page: Set[str] = set()
        for block in blocks:
            if len(block) < MIN_BLOCK_LENGTH:
                continue
            norm = _normalize_block(block)
            if norm not in seen_in_page:
                seen_in_page.add(norm)
                block_page_count[norm] += 1

    threshold = max(2, int(num_pages * REPEAT_THRESHOLD))
    repeated = {norm for norm, count in block_page_count.items() if count >= threshold}

    return repeated


def remove_repeated_blocks(content: str, repeated: Set[str]) -> str:
    """Remove blocks from content that match the repeated set."""
    if not repeated:
        return content

    blocks = _split_into_blocks(content)
    kept: List[str] = []

    for block in blocks:
        norm = _normalize_block(block)
        if len(block) >= MIN_BLOCK_LENGTH and norm in repeated:
            continue
        kept.append(block)

    return "\n\n".join(kept)


def deduplicate_crawl_output(raw_dir: Path, max_sample: int = 30) -> Tuple[int, int]:
    """Run cross-page deduplication on all markdown files in raw_dir.

    1. Read up to max_sample files to find repeated blocks
    2. Remove repeated blocks from ALL files
    3. Re-write cleaned files

    Returns (num_files_cleaned, num_blocks_removed).
    """
    md_files = sorted(raw_dir.rglob("*.md"))
    if len(md_files) < MIN_PAGES_FOR_DEDUP:
        print(f"  [dedup] Only {len(md_files)} files, skipping (need {MIN_PAGES_FOR_DEDUP}+)", file=sys.stderr)
        return 0, 0

    # Read sample files
    sample_files = md_files[:max_sample]
    file_contents: Dict[str, str] = {}
    for f in sample_files:
        try:
            file_contents[str(f)] = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

    # Find repeated blocks
    repeated = find_repeated_blocks(file_contents)
    if not repeated:
        print(f"  [dedup] No repeated blocks found across {len(sample_files)} pages", file=sys.stderr)
        return 0, 0

    print(f"  [dedup] Found {len(repeated)} repeated blocks across {len(sample_files)} pages", file=sys.stderr)
    for norm in sorted(repeated)[:5]:
        preview = norm[:80]
        print(f"    ✗ \"{preview}...\"", file=sys.stderr)
    if len(repeated) > 5:
        print(f"    ... and {len(repeated) - 5} more", file=sys.stderr)

    # Remove repeated blocks from ALL files
    total_removed = 0
    files_cleaned = 0

    for f in md_files:
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        blocks_before = len(_split_into_blocks(content))
        cleaned = remove_repeated_blocks(content, repeated)
        blocks_after = len(_split_into_blocks(cleaned))

        removed = blocks_before - blocks_after
        if removed > 0:
            # Normalize whitespace after removal
            cleaned = re.sub(r"\n{4,}", "\n\n\n", cleaned).strip()
            f.write_text(cleaned, encoding="utf-8")
            total_removed += removed
            files_cleaned += 1

    print(f"  [dedup] Removed {total_removed} repeated blocks from {files_cleaned} files", file=sys.stderr)
    return files_cleaned, total_removed
