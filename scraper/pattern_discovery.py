"""Pattern discovery for identifying recurring non-content patterns in docs."""
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict
from collections import Counter, defaultdict


@dataclass
class PatternCandidate:
    """Candidate artifact pattern found in analysis."""
    pattern: str
    count: int
    percentage: float
    sample_contexts: List[str]
    suggested_regex: str


def tokenize_line(line: str) -> List[str]:
    """Extract meaningful tokens from a line."""
    # Remove markdown syntax
    line = re.sub(r'[#*_`\[\]\(\)]', ' ', line)
    # Split on whitespace
    tokens = line.split()
    # Filter to meaningful tokens (>2 chars, not numbers)
    return [t for t in tokens if len(t) > 2 and not t.isdigit()]


def is_likely_boilerplate(line: str) -> bool:
    """Check if a line looks like boilerplate rather than content."""
    boilerplate_indicators = [
        'cookie', 'consent', 'accept all', 'reject all',
        'subscribe', 'newsletter', 'enter your email',
        'back to top', 'scroll to top',
        'copyright', 'all rights reserved',
        'terms of service', 'privacy policy',
        'edit on github', 'edit this page',
        'last updated', 'last modified',
        'on this page', 'table of contents',
        'show more', 'show less', 'expand', 'collapse',
        'was this page helpful', 'feedback',
        'previous', 'next',
        'search docs', 'search...',
        'loading', 'spinner',
        'reload', 'clear',
        'fork', 'codesandbox', 'stackblitz',
    ]
    line_lower = line.lower()
    return any(ind in line_lower for ind in boilerplate_indicators)


def generate_regex(pattern: str) -> str:
    """Generate a regex pattern from a string."""
    # Escape special chars
    escaped = re.escape(pattern)
    # Make it a bit more flexible (optional whitespace)
    return escaped.replace(r'\ ', r'\s*')


def discover_patterns(directory: str, threshold: float = 0.3, min_occurrences: int = 3) -> List[PatternCandidate]:
    """Scan directory and discover recurring patterns.
    
    Args:
        directory: Path to scan
        threshold: Minimum percentage of files pattern must appear in
        min_occurrences: Minimum total occurrences
        
    Returns:
        List of PatternCandidate sorted by count
    """
    dir_path = Path(directory)
    
    # Collect all lines and track which files they're from
    all_lines = []
    line_to_files = defaultdict(set)
    
    md_files = list(dir_path.rglob("*.md"))
    total_files = len(md_files)
    
    if total_files == 0:
        return []
    
    for file_path in md_files:
        try:
            content = file_path.read_text(encoding='utf-8')
            for line in content.splitlines():
                line = line.strip()
                if line and len(line) > 5:  # Skip empty/very short lines
                    all_lines.append(line)
                    line_to_files[line].add(file_path)
        except Exception:
            continue
    
    # Count occurrences and file coverage
    line_counts = Counter(all_lines)
    
    candidates = []
    for line, count in line_counts.most_common():
        if count < min_occurrences:
            continue
            
        file_count = len(line_to_files[line])
        percentage = file_count / total_files
        
        if percentage >= threshold:
            # Check if it's boilerplate
            is_boilerplate = is_likely_boilerplate(line)
            
            # Get sample contexts (up to 3)
            contexts = []
            for fp in list(line_to_files[line])[:3]:
                try:
                    content = fp.read_text(encoding='utf-8')
                    idx = content.find(line)
                    if idx >= 0:
                        start = max(0, idx - 50)
                        end = min(len(content), idx + len(line) + 50)
                        contexts.append(content[start:end].replace('\n', ' '))
                except Exception:
                    continue
            
            candidates.append(PatternCandidate(
                pattern=line[:100],  # Truncate very long lines
                count=count,
                percentage=percentage,
                sample_contexts=contexts,
                suggested_regex=generate_regex(line[:50])
            ))
    
    # Sort by count descending
    candidates.sort(key=lambda x: x.count, reverse=True)
    return candidates


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Discover recurring patterns in markdown docs")
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("--threshold", "-t", type=float, default=0.3,
                        help="Minimum percentage of files (default: 0.3)")
    parser.add_argument("--min-occurrences", "-m", type=int, default=3,
                        help="Minimum total occurrences (default: 3)")
    parser.add_argument("--top", "-n", type=int, default=20,
                        help="Show top N patterns (default: 20)")
    
    args = parser.parse_args()
    
    print(f"Scanning {args.directory}...")
    candidates = discover_patterns(
        args.directory,
        threshold=args.threshold,
        min_occurrences=args.min_occurrences
    )
    
    print(f"\nFound {len(candidates)} patterns:\n")
    print(f"{'Count':>6} {'Pct':>5} {'Pattern':<60} {'Regex Hint'}")
    print("-" * 100)
    
    for c in candidates[:args.top]:
        pattern_display = c.pattern[:57] + "..." if len(c.pattern) > 60 else c.pattern
        print(f"{c.count:>6} {c.percentage*100:>4.0f}% {pattern_display:<60} {c.suggested_regex[:30]}...")


if __name__ == "__main__":
    main()
