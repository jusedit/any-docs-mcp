"""HTML residue audit script for analyzing markdown output quality."""
import re
import json
import sys
from pathlib import Path
from collections import Counter
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))


class HTMLResidueAuditor:
    """Audit markdown files for HTML residue patterns."""
    
    # Common HTML tags that indicate residue
    HTML_TAG_PATTERNS = [
        r'<div[^>]*>',
        r'</div>',
        r'<span[^>]*>',
        r'</span>',
        r'<script[^>]*>',
        r'</script>',
        r'<style[^>]*>',
        r'</style>',
        r'<iframe[^>]*>',
        r'</iframe>',
        r'<nav[^>]*>',
        r'</nav>',
        r'<aside[^>]*>',
        r'</aside>',
        r'<footer[^>]*>',
        r'</footer>',
        r'<header[^>]*>',
        r'</header>',
        r'<svg[^>]*>',
        r'</svg>',
        r'<button[^>]*>',
        r'</button>',
        r'<input[^>]*>',
        r'<select[^>]*>',
        r'<textarea[^>]*>',
        r'<form[^>]*>',
        r'</form>',
        r'<table[^>]*>',
        r'</table>',
        r'<tbody[^>]*>',
        r'</tbody>',
        r'<tr[^>]*>',
        r'</tr>',
        r'<td[^>]*>',
        r'</td>',
        r'<th[^>]*>',
        r'</th>',
        r'<img[^>]*>',
        r'<br[^>]*>',
        r'<hr[^>]*>',
        r'<p[^>]*>',
        r'</p>',
        r'<a[^>]*>',
        r'</a>',
        r'<ul[^>]*>',
        r'</ul>',
        r'<ol[^>]*>',
        r'</ol>',
        r'<li[^>]*>',
        r'</li>',
        r'<strong[^>]*>',
        r'</strong>',
        r'<em[^>]*>',
        r'</em>',
        r'<code[^>]*>',
        r'</code>',
        r'<pre[^>]*>',
        r'</pre>',
        r'<blockquote[^>]*>',
        r'</blockquote>',
        r'<h1[^>]*>',
        r'</h1>',
        r'<h2[^>]*>',
        r'</h2>',
        r'<h3[^>]*>',
        r'</h3>',
        r'<h4[^>]*>',
        r'</h4>',
        r'<h5[^>]*>',
        r'</h5>',
        r'<h6[^>]*>',
        r'</h6>',
    ]
    
    # Tailwind-specific patterns
    TAILWIND_PATTERNS = [
        r'class="[^"]*tailwind[^"]*"',
        r'class="[^"]*bg-[^"]*"',
        r'class="[^"]*text-[^"]*"',
        r'class="[^"]*p-[^"]*"',
        r'class="[^"]*m-[^"]*"',
        r'class="[^"]*flex[^"]*"',
        r'class="[^"]*grid[^"]*"',
        r'class="[^"]*border[^"]*"',
        r'class="[^"]*rounded[^"]*"',
        r'class="[^"]*shadow[^"]*"',
        r'class="[^"]*hover:[^"]*"',
        r'class="[^"]*focus:[^"]*"',
        r'class="[^"]*active:[^"]*"',
        r'class="[^"]*w-[^"]*"',
        r'class="[^"]*h-[^"]*"',
        r'class="[^"]*min-w[^"]*"',
        r'class="[^"]*max-w[^"]*"',
        r'class="[^"]*min-h[^"]*"',
        r'class="[^"]*max-h[^"]*"',
        r'class="[^"]*opacity-[^"]*"',
        r'class="[^"]*z-[^"]*"',
        r'class="[^"]*relative[^"]*"',
        r'class="[^"]*absolute[^"]*"',
        r'class="[^"]*fixed[^"]*"',
        r'class="[^"]*sticky[^"]*"',
        r'class="[^"]*hidden[^"]*"',
        r'class="[^"]*block[^"]*"',
        r'class="[^"]*inline[^"]*"',
        r'class="[^"]*inline-block[^"]*"',
        r'class="[^"]*contents[^"]*"',
    ]
    
    def __init__(self):
        self.total_files = 0
        self.files_with_residue = 0
        self.total_residue_count = 0
        self.tag_counts = Counter()
        self.file_residues = {}
    
    def audit_file(self, file_path: Path) -> Dict:
        """Audit a single markdown file for HTML residue."""
        content = file_path.read_text(encoding='utf-8')
        
        file_residues = []
        
        # Check for HTML tags
        for pattern in self.HTML_TAG_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                for match in matches:
                    file_residues.append({
                        'type': 'html_tag',
                        'pattern': pattern,
                        'match': match[:50],  # Truncate for readability
                        'line': self._find_line_number(content, match)
                    })
                    self.tag_counts[match.lower()] += 1
        
        # Check for Tailwind patterns
        for pattern in self.TAILWIND_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                for match in matches:
                    file_residues.append({
                        'type': 'tailwind_class',
                        'pattern': pattern,
                        'match': match[:50],
                        'line': self._find_line_number(content, match)
                    })
                    self.tag_counts['tailwind_class'] += 1
        
        return {
            'file': str(file_path),
            'residue_count': len(file_residues),
            'residues': file_residues
        }
    
    def _find_line_number(self, content: str, match: str) -> int:
        """Find line number of a match in content."""
        pos = content.find(match)
        if pos == -1:
            return 0
        return content[:pos].count('\n') + 1
    
    def audit_directory(self, directory: Path) -> Dict:
        """Audit all markdown files in a directory."""
        md_files = list(directory.rglob("*.md"))
        
        results = {
            'directory': str(directory),
            'total_files': len(md_files),
            'files_with_residue': 0,
            'total_residue_count': 0,
            'top_tags': [],
            'files': []
        }
        
        for md_file in md_files:
            file_result = self.audit_file(md_file)
            results['files'].append(file_result)
            
            if file_result['residue_count'] > 0:
                results['files_with_residue'] += 1
                results['total_residue_count'] += file_result['residue_count']
        
        # Get top 5 most common tags
        results['top_tags'] = self.tag_counts.most_common(5)
        
        return results
    
    def generate_report(self, results: Dict) -> str:
        """Generate a human-readable audit report."""
        report = []
        report.append("=" * 60)
        report.append("HTML RESIDUE AUDIT REPORT")
        report.append("=" * 60)
        report.append(f"Directory: {results['directory']}")
        report.append(f"Total files scanned: {results['total_files']}")
        report.append(f"Files with residue: {results['files_with_residue']}")
        report.append(f"Total residue instances: {results['total_residue_count']}")
        report.append("")
        
        if results['top_tags']:
            report.append("TOP 5 HTML RESIDUE PATTERNS:")
            report.append("-" * 30)
            for tag, count in results['top_tags']:
                report.append(f"  {tag}: {count} instances")
            report.append("")
        
        # Show files with most residue
        files_with_residue = [f for f in results['files'] if f['residue_count'] > 0]
        files_with_residue.sort(key=lambda x: x['residue_count'], reverse=True)
        
        if files_with_residue:
            report.append("FILES WITH MOST RESIDUE:")
            report.append("-" * 30)
            for file_result in files_with_residue[:10]:  # Top 10
                report.append(f"  {file_result['file']}: {file_result['residue_count']} instances")
            report.append("")
        
        report.append("=" * 60)
        
        return '\n'.join(report)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Audit markdown files for HTML residue")
    parser.add_argument("directory", type=str, help="Directory containing .md files to audit")
    parser.add_argument("--output", "-o", type=str, help="Output JSON file for detailed results")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed residue information")
    args = parser.parse_args()
    
    directory = Path(args.directory)
    if not directory.exists():
        print(f"Error: Directory {directory} does not exist")
        sys.exit(1)
    
    auditor = HTMLResidueAuditor()
    results = auditor.audit_directory(directory)
    
    # Print report
    print(auditor.generate_report(results))
    
    # Save detailed results if requested
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nDetailed results saved to: {args.output}")
    
    # Exit with error code if residue found
    if results['total_residue_count'] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
