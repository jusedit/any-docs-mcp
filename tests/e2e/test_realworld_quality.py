"""
Real-World Quality Benchmark

Tests the full MCP pipeline against REAL scraped documentation from AppData.
Evaluates across 5 dimensions:
  1. Markdown structure quality (headings, code blocks, encoding)
  2. MCP index quality (sections, coverage, build time)
  3. Search relevance (precision@1, precision@3, MRR)
  4. Overview & TOC quality
  5. Code example retrieval

Produces a quality dashboard JSON: tests/e2e/quality-dashboard.json
"""
import json
import os
import sys
import re
import subprocess
import time
import pytest
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field

SCRAPER_DIR = Path(__file__).parent.parent.parent / "scraper"
sys.path.insert(0, str(SCRAPER_DIR))

APPDATA_DOCS = Path(os.getenv("APPDATA", "")) / "AnyDocsMCP" / "docs"
MCP_SERVER_DIR = Path(__file__).parent.parent.parent / "mcp-server"
DASHBOARD_PATH = Path(__file__).parent / "quality-dashboard.json"
QUERY_SUITE_PATH = Path(__file__).parent.parent / "fixtures" / "real-world" / "query-suite.json"

# 10 reference doc-sets
REFERENCE_DOCS = [
    "react", "fastapi", "tailwind", "kubernetes", "django",
    "hyperapp-github", "onoffice", "synthflow", "golang", "rust-book",
]


# ---- Data classes for scoring ----

@dataclass
class MarkdownQuality:
    total_files: int = 0
    total_size_bytes: int = 0
    avg_file_size_bytes: float = 0
    total_headings: int = 0
    total_code_blocks: int = 0
    files_with_code: int = 0
    encoding_errors: int = 0      # mojibake patterns found
    html_residue_count: int = 0   # leftover HTML tags
    empty_files: int = 0
    score: float = 0.0            # 0-1

@dataclass
class MCPIndexQuality:
    total_sections: int = 0
    total_files_indexed: int = 0
    build_time_ms: float = 0
    sections_with_code: int = 0
    sections_with_source_url: int = 0
    avg_content_length: float = 0
    score: float = 0.0

@dataclass
class SearchRelevance:
    queries_tested: int = 0
    precision_at_1: float = 0.0
    precision_at_3: float = 0.0
    mrr: float = 0.0             # Mean Reciprocal Rank
    zero_result_queries: int = 0
    score: float = 0.0

@dataclass
class OverviewQuality:
    overview_length: int = 0
    toc_files_with_entries: int = 0
    toc_total_entries: int = 0
    score: float = 0.0

@dataclass
class DocSetReport:
    name: str = ""
    version: str = ""
    markdown: MarkdownQuality = field(default_factory=MarkdownQuality)
    mcp_index: MCPIndexQuality = field(default_factory=MCPIndexQuality)
    search: SearchRelevance = field(default_factory=SearchRelevance)
    overview: OverviewQuality = field(default_factory=OverviewQuality)
    overall_score: float = 0.0


# ---- Markdown analysis (Python side) ----

MOJIBAKE_PATTERNS = [
    r"\xc3\xa2\xc2\x80",   # Double-encoded UTF-8
    r"\xc2\xb6",            # Orphan pilcrow
    r"\xc3\x83",            # Mojibake A-tilde
    r"\xe2\x80\x99",        # This is actually correct right-quote in UTF-8
]
MOJIBAKE_RE = re.compile(
    r"(\u00e2\u0080[\u0090-\u00ff])"   # Common mojibake range
    r"|(\u00c2[\u00a0-\u00bf])"        # Orphan Latin supplement
    r"|(\u00c3[\u0080-\u00bf])"        # Double-encoded accents
)
HTML_TAG_RE = re.compile(r"<(?:div|span|section|header|footer|aside|iframe|script|style|button|form|input|select|option|label|table|thead|tbody|tr|td|th)\b", re.IGNORECASE)


def analyze_markdown_quality(docs_path: Path) -> MarkdownQuality:
    """Analyze markdown quality of all .md files in a directory."""
    q = MarkdownQuality()
    md_files = list(docs_path.glob("*.md"))
    q.total_files = len(md_files)
    if not md_files:
        return q

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        size = len(content.encode("utf-8"))
        q.total_size_bytes += size

        if len(content.strip()) < 50:
            q.empty_files += 1
            continue

        # Headings
        headings = re.findall(r"^#{1,6}\s", content, re.MULTILINE)
        q.total_headings += len(headings)

        # Code blocks
        code_blocks = re.findall(r"```\w*", content)
        block_count = len(code_blocks) // 2  # opening + closing
        q.total_code_blocks += block_count
        if block_count > 0:
            q.files_with_code += 1

        # Encoding errors (mojibake)
        q.encoding_errors += len(MOJIBAKE_RE.findall(content))

        # HTML residue
        q.html_residue_count += len(HTML_TAG_RE.findall(content))

    q.avg_file_size_bytes = q.total_size_bytes / q.total_files if q.total_files else 0

    # Score: weighted combination
    files_ok = max(0, q.total_files - q.empty_files) / max(q.total_files, 1)
    has_headings = min(q.total_headings / max(q.total_files, 1) / 3, 1.0)  # expect ~3 headings/file
    has_code = q.files_with_code / max(q.total_files, 1)
    encoding_clean = max(0, 1.0 - q.encoding_errors / max(q.total_files, 1))
    html_clean = max(0, 1.0 - q.html_residue_count / max(q.total_files * 2, 1))

    q.score = round(
        files_ok * 0.2 + has_headings * 0.25 + has_code * 0.2 +
        encoding_clean * 0.2 + html_clean * 0.15, 3
    )
    return q


# ---- TypeScript MCP evaluation (via subprocess) ----

def run_mcp_evaluation(docs_path: str, doc_name: str, queries: List[dict]) -> dict:
    """Run the TypeScript MCP evaluation script and return results."""
    eval_script = MCP_SERVER_DIR / "src" / "__tests__" / "eval-realworld.ts"
    if not eval_script.exists():
        return {"error": "eval-realworld.ts not found"}

    input_data = json.dumps({
        "docsPath": docs_path,
        "docName": doc_name,
        "queries": queries,
    })

    result = subprocess.run(
        f'npx tsx "{eval_script}"',
        input=input_data,
        cwd=str(MCP_SERVER_DIR),
        capture_output=True,
        text=True,
        timeout=30,
        shell=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        return {"error": result.stderr[:500]}

    # Parse JSON output from the script
    try:
        for line in result.stdout.strip().split("\n"):
            if line.startswith("{"):
                return json.loads(line)
        return {"error": "No JSON output from eval script"}
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON: {result.stdout[:200]}"}


# ---- Test class ----

class TestRealWorldQuality:
    """Real-world quality benchmark across all reference doc-sets."""

    @pytest.fixture(autouse=True, scope="class")
    def setup(self, request):
        if not APPDATA_DOCS.exists():
            pytest.skip("AppData docs not available")

        # Find available doc-sets
        available = []
        for name in REFERENCE_DOCS:
            doc_dir = APPDATA_DOCS / name
            if doc_dir.exists():
                # Find latest version with .md files
                versions = sorted(
                    [d for d in doc_dir.iterdir() if d.is_dir() and d.name.startswith("v")],
                    key=lambda d: int(d.name[1:]) if d.name[1:].isdigit() else 0,
                    reverse=True,
                )
                for v in versions:
                    if list(v.glob("*.md")):
                        available.append((name, v.name, str(v)))
                        break

        request.cls.available_docs = available
        request.cls.reports: Dict[str, DocSetReport] = {}

        # Load query suite
        request.cls.queries = []
        if QUERY_SUITE_PATH.exists():
            with open(QUERY_SUITE_PATH) as f:
                data = json.load(f)
                request.cls.queries = data.get("queries", [])

    def test_markdown_quality_per_docset(self):
        """Evaluate markdown structure quality for each doc-set."""
        print("\n" + "=" * 70)
        print("  MARKDOWN STRUCTURE QUALITY")
        print("=" * 70)

        for name, version, path in self.available_docs:
            docs_path = Path(path)
            mq = analyze_markdown_quality(docs_path)

            report = self.reports.get(name, DocSetReport(name=name, version=version))
            report.markdown = mq
            self.reports[name] = report

            status = "GOOD" if mq.score >= 0.6 else "WARN" if mq.score >= 0.4 else "POOR"
            print(
                f"  {name:20s} | {mq.total_files:4d} files | "
                f"{mq.total_headings:5d} headings | {mq.total_code_blocks:4d} code | "
                f"enc_err={mq.encoding_errors:3d} | html={mq.html_residue_count:3d} | "
                f"score={mq.score:.2f} [{status}]"
            )

        # At least some doc-sets should score well
        scores = [r.markdown.score for r in self.reports.values()]
        avg = sum(scores) / len(scores) if scores else 0
        print(f"\n  Average markdown quality: {avg:.2f}")
        assert avg > 0.3, f"Average markdown quality too low: {avg:.2f}"

    def test_mcp_index_quality(self):
        """Evaluate MCP indexing quality for each doc-set."""
        print("\n" + "=" * 70)
        print("  MCP INDEX QUALITY")
        print("=" * 70)

        eval_script = MCP_SERVER_DIR / "src" / "__tests__" / "eval-realworld.ts"
        if not eval_script.exists():
            pytest.skip("eval-realworld.ts not created yet")

        for name, version, path in self.available_docs:
            queries_for_doc = [q for q in self.queries if q["doc_name"] == name]
            result = run_mcp_evaluation(path, name, queries_for_doc)

            if "error" in result:
                print(f"  {name:20s} | ERROR: {result['error'][:60]}")
                continue

            idx = result.get("index", {})
            report = self.reports.get(name, DocSetReport(name=name, version=version))
            report.mcp_index = MCPIndexQuality(
                total_sections=idx.get("totalSections", 0),
                total_files_indexed=idx.get("totalFiles", 0),
                build_time_ms=idx.get("buildTimeMs", 0),
                sections_with_code=idx.get("sectionsWithCode", 0),
                sections_with_source_url=idx.get("sectionsWithSourceUrl", 0),
                avg_content_length=idx.get("avgContentLength", 0),
            )

            # Score
            sec = report.mcp_index.total_sections
            code_ratio = report.mcp_index.sections_with_code / max(sec, 1)
            build_ok = 1.0 if report.mcp_index.build_time_ms < 5000 else 0.5
            report.mcp_index.score = round(
                min(sec / 50, 1.0) * 0.3 + code_ratio * 0.3 + build_ok * 0.2 +
                min(report.mcp_index.avg_content_length / 500, 1.0) * 0.2, 3
            )

            # Search relevance from TS evaluation
            sr = result.get("search", {})
            report.search = SearchRelevance(
                queries_tested=sr.get("queriesTested", 0),
                precision_at_1=sr.get("precisionAt1", 0),
                precision_at_3=sr.get("precisionAt3", 0),
                mrr=sr.get("mrr", 0),
                zero_result_queries=sr.get("zeroResultQueries", 0),
            )
            report.search.score = round(
                report.search.precision_at_1 * 0.4 +
                report.search.precision_at_3 * 0.3 +
                report.search.mrr * 0.3, 3
            )

            # Overview
            ov = result.get("overview", {})
            report.overview = OverviewQuality(
                overview_length=ov.get("overviewLength", 0),
                toc_files_with_entries=ov.get("tocFilesWithEntries", 0),
                toc_total_entries=ov.get("tocTotalEntries", 0),
            )
            report.overview.score = round(
                min(report.overview.overview_length / 1000, 1.0) * 0.4 +
                (report.overview.toc_files_with_entries / max(report.mcp_index.total_files_indexed, 1)) * 0.3 +
                min(report.overview.toc_total_entries / 20, 1.0) * 0.3, 3
            )

            self.reports[name] = report

            print(
                f"  {name:20s} | {sec:5d} sections | "
                f"build={report.mcp_index.build_time_ms:6.0f}ms | "
                f"p@1={report.search.precision_at_1:.2f} | "
                f"p@3={report.search.precision_at_3:.2f} | "
                f"MRR={report.search.mrr:.2f} | "
                f"idx={report.mcp_index.score:.2f} srch={report.search.score:.2f}"
            )

    def test_generate_quality_dashboard(self):
        """Generate the final quality dashboard JSON."""
        # Compute overall scores
        for report in self.reports.values():
            weights = {"markdown": 0.25, "mcp_index": 0.25, "search": 0.30, "overview": 0.20}
            report.overall_score = round(
                report.markdown.score * weights["markdown"] +
                report.mcp_index.score * weights["mcp_index"] +
                report.search.score * weights["search"] +
                report.overview.score * weights["overview"], 3
            )

        # Build dashboard
        dashboard = {
            "generated_at": datetime.now().isoformat(),
            "doc_sets_evaluated": len(self.reports),
            "per_doc_set": {},
            "aggregate": {},
        }

        for name, report in sorted(self.reports.items()):
            dashboard["per_doc_set"][name] = asdict(report)

        # Aggregate
        reports = list(self.reports.values())
        if reports:
            dashboard["aggregate"] = {
                "avg_overall_score": round(sum(r.overall_score for r in reports) / len(reports), 3),
                "avg_markdown_score": round(sum(r.markdown.score for r in reports) / len(reports), 3),
                "avg_index_score": round(sum(r.mcp_index.score for r in reports) / len(reports), 3),
                "avg_search_score": round(sum(r.search.score for r in reports) / len(reports), 3),
                "avg_overview_score": round(sum(r.overview.score for r in reports) / len(reports), 3),
                "total_files": sum(r.markdown.total_files for r in reports),
                "total_sections": sum(r.mcp_index.total_sections for r in reports),
                "total_encoding_errors": sum(r.markdown.encoding_errors for r in reports),
                "total_html_residue": sum(r.markdown.html_residue_count for r in reports),
            }

        # Write dashboard
        DASHBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(DASHBOARD_PATH, "w") as f:
            json.dump(dashboard, f, indent=2)

        # Print summary
        print("\n" + "=" * 70)
        print("  QUALITY DASHBOARD SUMMARY")
        print("=" * 70)
        print(f"  Doc-sets evaluated: {len(reports)}")
        if "avg_overall_score" in dashboard.get("aggregate", {}):
            agg = dashboard["aggregate"]
            print(f"  Avg overall score:  {agg['avg_overall_score']:.2f}")
            print(f"  Avg markdown:       {agg['avg_markdown_score']:.2f}")
            print(f"  Avg MCP index:      {agg['avg_index_score']:.2f}")
            print(f"  Avg search:         {agg['avg_search_score']:.2f}")
            print(f"  Avg overview:       {agg['avg_overview_score']:.2f}")
            print(f"  Total files:        {agg['total_files']}")
            print(f"  Total sections:     {agg['total_sections']}")
            print(f"  Encoding errors:    {agg['total_encoding_errors']}")
            print(f"  HTML residue:       {agg['total_html_residue']}")
        print(f"\n  Dashboard written to: {DASHBOARD_PATH}")

        assert len(reports) >= 3, f"Expected >= 3 doc-sets evaluated, got {len(reports)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
