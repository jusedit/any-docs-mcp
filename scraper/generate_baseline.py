"""Generate quality baseline metrics for golden fixture files."""
import json
import re
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class FileMetrics:
    """Quality metrics for a single golden file."""
    doc_set: str
    file_name: str
    char_count: int
    line_count: int
    heading_count: int
    code_block_count: int
    encoding_errors: int
    artifacts: int


def count_encoding_errors(content: str) -> int:
    """Count encoding defects in content."""
    # Mojibake patterns
    mojibake_patterns = [
        r'â[€\x80-â\x9f]',  # Curly quotes, dashes
        r'Ã[\xa0-Ã\xbf]',  # Accented chars
        r'Â[\x80-Â\xbf]',  # Orphan Latin supplement
    ]
    count = 0
    for pattern in mojibake_patterns:
        count += len(re.findall(pattern, content))
    return count


def count_artifacts(content: str) -> int:
    """Count UI artifacts in content."""
    artifact_patterns = [
        r'Show more',
        r'Show less', 
        r'On this page',
        r'ReloadClear',
        r'sp-pre-placeholder',
        r'Â¶',  # Permalink
        r'\[¶\]\(#'  # Permalink link
    ]
    count = 0
    for pattern in artifact_patterns:
        count += len(re.findall(pattern, content))
    return count


def analyze_file(doc_set: str, file_path: Path) -> FileMetrics:
    """Analyze a single markdown file and return metrics."""
    content = file_path.read_text(encoding='utf-8')
    
    return FileMetrics(
        doc_set=doc_set,
        file_name=file_path.name,
        char_count=len(content),
        line_count=len(content.splitlines()),
        heading_count=len(re.findall(r'^#{1,6}\s', content, re.MULTILINE)),
        code_block_count=len(re.findall(r'```[\w]*', content)),
        encoding_errors=count_encoding_errors(content),
        artifacts=count_artifacts(content)
    )


def scan_golden_files(fixtures_dir: str = "tests/fixtures/real-world") -> List[FileMetrics]:
    """Scan all golden directories and collect metrics."""
    fixtures_path = Path(fixtures_dir)
    metrics = []
    
    for doc_dir in fixtures_path.iterdir():
        if not doc_dir.is_dir():
            continue
            
        golden_dir = doc_dir / "golden"
        if not golden_dir.exists():
            continue
            
        for md_file in golden_dir.glob("*.md"):
            metrics.append(analyze_file(doc_dir.name, md_file))
    
    return metrics


def generate_baseline(fixtures_dir: str = "tests/fixtures/real-world") -> dict:
    """Generate quality baseline report."""
    metrics = scan_golden_files(fixtures_dir)
    
    baseline = {
        "version": "1.0.0",
        "generated_at": "",
        "files": {},
        "summary": {
            "total_files": len(metrics),
            "total_chars": sum(m.char_count for m in metrics),
            "total_headings": sum(m.heading_count for m in metrics),
            "total_code_blocks": sum(m.code_block_count for m in metrics),
            "total_encoding_errors": sum(m.encoding_errors for m in metrics),
            "total_artifacts": sum(m.artifacts for m in metrics)
        }
    }
    
    for m in metrics:
        key = f"{m.doc_set}/{m.file_name}"
        baseline["files"][key] = {
            "char_count": m.char_count,
            "line_count": m.line_count,
            "heading_count": m.heading_count,
            "code_block_count": m.code_block_count,
            "encoding_errors": m.encoding_errors,
            "artifacts": m.artifacts
        }
    
    return baseline


def main():
    """CLI entry point."""
    import argparse
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description="Generate quality baseline for golden fixtures")
    parser.add_argument("--fixtures-dir", "-f", default="tests/fixtures/real-world",
                        help="Path to fixtures directory")
    parser.add_argument("--output", "-o", default="tests/fixtures/real-world/quality_baseline.json",
                        help="Output file path")
    
    args = parser.parse_args()
    
    print("Scanning golden fixtures...")
    baseline = generate_baseline(args.fixtures_dir)
    baseline["generated_at"] = datetime.utcnow().isoformat() + "Z"
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(baseline, f, indent=2)
    
    print(f"Baseline written to: {output_path}")
    print(f"Total files: {baseline['summary']['total_files']}")
    print(f"Total chars: {baseline['summary']['total_chars']:,}")
    print(f"Encoding errors: {baseline['summary']['total_encoding_errors']}")
    print(f"Artifacts: {baseline['summary']['total_artifacts']}")


if __name__ == "__main__":
    main()
