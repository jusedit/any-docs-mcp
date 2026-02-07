"""Encoding audit script for detecting defects in markdown files."""
import json
import re
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from collections import defaultdict


@dataclass
class Defect:
    """Single encoding defect found in a file."""
    category: str
    pattern_matched: str
    file_path: str
    line_number: int
    context: str


@dataclass
class AuditReport:
    """Complete audit report for a directory."""
    total_files: int
    affected_files: int
    defects_by_category: Dict[str, int]
    defects: List[Defect]


class EncodingAuditor:
    """Scans markdown files for encoding defects."""
    
    # Patterns for each defect category
    PATTERNS = {
        "mojibake": [
            (r'â[€\x80-\x9f]', "Mojibake curly quote/dash"),
            (r'Ã[\xa0-\xbf]', "Mojibake accented char"),
        ],
        "broken_latin": [
            (r'Â[\x80-\xbf]', "Orphan Latin-1 supplement"),
        ],
        "permalink_anchors": [
            (r'Â¶', "Permalink anchor character"),
            (r'\[¶\]\(#', "Permalink link in heading"),
            (r'\[\]\(#', "Empty anchor link"),
        ],
        "html_entities": [
            (r'&amp;|&lt;|&gt;|&quot;|&#\d+;', "HTML entity"),
        ]
    }
    
    def __init__(self):
        self.defects: List[Defect] = []
    
    def scan_file(self, file_path: Path) -> List[Defect]:
        """Scan a single file for defects."""
        defects = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.splitlines()
        except Exception as e:
            return [Defect(
                category="read_error",
                pattern_matched=str(e),
                file_path=str(file_path),
                line_number=0,
                context=""
            )]
        
        for line_num, line in enumerate(lines, 1):
            for category, patterns in self.PATTERNS.items():
                for pattern, description in patterns:
                    for match in re.finditer(pattern, line):
                        # Get context (±20 chars around match)
                        start = max(0, match.start() - 20)
                        end = min(len(line), match.end() + 20)
                        context = line[start:end]
                        
                        defects.append(Defect(
                            category=category,
                            pattern_matched=match.group(),
                            file_path=str(file_path),
                            line_number=line_num,
                            context=context
                        ))
        
        return defects
    
    def scan_directory(self, directory: str) -> AuditReport:
        """Scan all markdown files in directory."""
        dir_path = Path(directory)
        self.defects = []
        
        # Find all markdown files
        md_files = list(dir_path.rglob("*.md"))
        
        for file_path in md_files:
            file_defects = self.scan_file(file_path)
            self.defects.extend(file_defects)
        
        # Calculate summary
        affected_files = len(set(d.file_path for d in self.defects if d.category != "read_error"))
        defects_by_category = defaultdict(int)
        for defect in self.defects:
            defects_by_category[defect.category] += 1
        
        return AuditReport(
            total_files=len(md_files),
            affected_files=affected_files,
            defects_by_category=dict(defects_by_category),
            defects=self.defects
        )
    
    def scan_text(self, text: str) -> List[Defect]:
        """Scan a text string for defects (for testing)."""
        defects = []
        lines = text.splitlines()
        
        for line_num, line in enumerate(lines, 1):
            for category, patterns in self.PATTERNS.items():
                for pattern, description in patterns:
                    for match in re.finditer(pattern, line):
                        start = max(0, match.start() - 20)
                        end = min(len(line), match.end() + 20)
                        context = line[start:end]
                        
                        defects.append(Defect(
                            category=category,
                            pattern_matched=match.group(),
                            file_path="<inline>",
                            line_number=line_num,
                            context=context
                        ))
        
        return defects


def format_report(report: AuditReport) -> dict:
    """Format report as JSON-serializable dict."""
    return {
        "total_files": report.total_files,
        "affected_files": report.affected_files,
        "defects_by_category": report.defects_by_category,
        "defects": [
            {
                "category": d.category,
                "pattern_matched": d.pattern_matched,
                "file_path": d.file_path,
                "line_number": d.line_number,
                "context": d.context
            }
            for d in report.defects
        ]
    }


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Audit markdown files for encoding defects"
    )
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("--output", "-o", help="Output JSON file")
    parser.add_argument("--summary", "-s", action="store_true",
                        help="Show summary only")
    
    args = parser.parse_args()
    
    auditor = EncodingAuditor()
    report = auditor.scan_directory(args.directory)
    
    if args.summary:
        print(f"Files scanned: {report.total_files}")
        print(f"Files affected: {report.affected_files}")
        print("\nDefects by category:")
        for category, count in report.defects_by_category.items():
            print(f"  {category}: {count}")
    elif args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(format_report(report), f, indent=2)
        print(f"Report written to: {args.output}")
    else:
        # Print to stdout
        print(json.dumps(format_report(report), indent=2))


if __name__ == "__main__":
    main()
