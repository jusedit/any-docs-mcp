"""Main pipeline orchestrator — ties all FR1-FR5 modules together.

Flow:
  Start URL → Engine Selector → Discovery Worker → LLM Analyzer
  → Crawl (small sample) → LLM Selector Refinement → Crawl (full)
  → Cross-page Dedup → LLM Grouper → AGENTS.md

Two-pass crawl strategy:
  Pass 1: Crawl ~5 sample pages, show output to LLM for selector refinement
  Pass 2: Re-crawl all pages with improved selectors
  Post:   Cross-page dedup removes any remaining repeated UI blocks
"""
import shutil
import sys
import time
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

from models import EngineMode, PipelineConfig
from engine_selector import select_engine
from discovery import DiscoveryWorker
from llm_analyzer import LLMAnalyzer
from crawler import Crawler
from grouper import Grouper
from dedup import deduplicate_crawl_output

MIN_CRAWL_SUCCESS_RATE = 0.20
MAX_CRAWL_RETRIES = 1
SAMPLE_CRAWL_SIZE = 5


class Pipeline:
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self) -> Path:
        """Execute the full scraping pipeline.

        Returns path to generated AGENTS.md.
        """
        start = time.time()
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"  Scraper v2 Pipeline: {self.config.start_url}", file=sys.stderr)
        print(f"  Output: {self.output_dir}", file=sys.stderr)
        print(f"{'='*60}\n", file=sys.stderr)

        parsed = urlparse(self.config.start_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        # --- FR1: Engine Selection ---
        print("[1/7] Engine Selection...", file=sys.stderr)
        decision = select_engine(
            self.config.start_url,
            threshold=self.config.engine_diff_threshold,
        )
        engine_mode = decision.mode
        print(f"  → Engine: {engine_mode.value} ({decision.reason})\n", file=sys.stderr)

        report_path = self.output_dir / "engine-decision.json"
        report_path.write_text(decision.model_dump_json(indent=2), encoding="utf-8")

        # --- FR2: Discovery ---
        print("[2/7] URL Discovery...", file=sys.stderr)
        discovery = DiscoveryWorker(engine_mode=engine_mode)
        frontier, start_html, sample_links = discovery.discover(
            self.config.start_url,
            max_sample_pages=10,
        )
        print(f"  → Frontier: {len(frontier)} URLs\n", file=sys.stderr)

        if not frontier:
            print("  ERROR: No URLs discovered. Aborting.", file=sys.stderr)
            return self.output_dir / "AGENTS.md"

        # --- FR3: LLM Analyzer ---
        print("[3/7] LLM Analysis (scope + selectors)...", file=sys.stderr)
        analyzer = LLMAnalyzer(model=self.config.llm_model_analyzer)
        analysis = analyzer.analyze(
            start_url=self.config.start_url,
            base_url=base_url,
            start_html=start_html,
            sample_links=sample_links,
        )

        # Filter frontier by scope rules
        full_frontier = frontier
        before = len(frontier)
        frontier = [r for r in frontier if analysis.scope_rules.url_matches(r.url)]
        print(f"  → Scope filter: {before} → {len(frontier)} URLs", file=sys.stderr)
        print(f"  → Content selector: {analysis.selector_spec.content_selector}", file=sys.stderr)
        print(f"  → Prune selectors: {len(analysis.selector_spec.prune_selectors)}\n", file=sys.stderr)

        # Save analysis
        analysis_path = self.output_dir / "llm-analysis.json"
        analysis_path.write_text(analysis.model_dump_json(indent=2), encoding="utf-8")

        # Cap at max_pages
        if len(frontier) > self.config.max_pages:
            print(f"  [WARNING] Capping frontier from {len(frontier)} to {self.config.max_pages}", file=sys.stderr)
            frontier = frontier[:self.config.max_pages]

        # --- FR4a: Sample crawl for selector refinement ---
        print("[4/7] Sample crawl for selector refinement...", file=sys.stderr)
        sample_size = min(SAMPLE_CRAWL_SIZE, len(frontier))
        sample_frontier = frontier[:sample_size]

        crawler = Crawler(
            engine_mode=engine_mode,
            selector_spec=analysis.selector_spec,
            output_dir=str(self.output_dir),
            max_workers=self.config.max_workers,
        )
        try:
            sample_manifest = crawler.crawl(sample_frontier)
        finally:
            crawler.close()

        success_rate = sample_manifest.total_pages / len(sample_frontier) if sample_frontier else 0
        print(f"  → Sample: {sample_manifest.total_pages}/{sample_size} pages (success rate: {success_rate:.1%})", file=sys.stderr)

        # --- FR4b: LLM Selector Refinement ---
        print("[5/7] LLM Selector Refinement...", file=sys.stderr)
        raw_dir = self.output_dir / "md" / "raw"
        sample_md_contents = self._read_sample_md(raw_dir, max_files=3)

        if sample_md_contents:
            refined_spec = analyzer.refine_selectors(
                current_analysis=analysis,
                sample_md_contents=sample_md_contents,
                start_url=self.config.start_url,
                start_html=start_html,
            )
            analysis.selector_spec = refined_spec

            # Save refined analysis
            analysis_path.write_text(analysis.model_dump_json(indent=2), encoding="utf-8")
        else:
            print(f"  [refine] No sample content available, skipping refinement", file=sys.stderr)

        # --- FR4c: Full crawl with refined selectors ---
        # Clean up sample crawl output
        if raw_dir.exists():
            shutil.rmtree(raw_dir)
            raw_dir.mkdir(parents=True, exist_ok=True)

        manifest = self._crawl_with_quality_check(
            frontier, engine_mode, analysis, analyzer,
            base_url, start_html, sample_links, full_frontier,
        )

        # --- FR4d: Cross-page dedup ---
        print("[6/7] Cross-page deduplication...", file=sys.stderr)
        deduplicate_crawl_output(raw_dir)

        # --- FR5: AGENTS.md index ---
        print("[7/7] AGENTS.md index generation...", file=sys.stderr)
        grouper = Grouper()
        agents_path = grouper.group_and_package(
            manifest=manifest,
            output_dir=str(self.output_dir),
            doc_name=self.config.name,
        )

        elapsed = time.time() - start
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"  Pipeline complete in {elapsed:.1f}s", file=sys.stderr)
        print(f"  Pages: {manifest.total_pages}", file=sys.stderr)
        print(f"  AGENTS.md: {agents_path}", file=sys.stderr)
        print(f"  Output: {self.output_dir}", file=sys.stderr)
        print(f"{'='*60}\n", file=sys.stderr)

        return agents_path

    def _read_sample_md(self, raw_dir: Path, max_files: int = 3) -> List[str]:
        """Read a few sample markdown files for LLM refinement."""
        contents = []
        if not raw_dir.exists():
            return contents
        for f in sorted(raw_dir.rglob("*.md"))[:max_files]:
            try:
                contents.append(f.read_text(encoding="utf-8", errors="replace"))
            except Exception:
                continue
        return contents

    def _crawl_with_quality_check(
        self, frontier, engine_mode, analysis, analyzer,
        base_url, start_html, sample_links, full_frontier,
    ):
        """Crawl with quality feedback loop.

        If crawl success rate is below MIN_CRAWL_SUCCESS_RATE, re-analyze
        selectors with LLM feedback and re-crawl up to MAX_CRAWL_RETRIES times.
        """
        for attempt in range(MAX_CRAWL_RETRIES + 1):
            attempt_label = f" (attempt {attempt + 1})" if attempt > 0 else ""
            step = "4/7" if attempt == 0 else "4/7"
            print(f"[{step}] Crawling & Transforming{attempt_label}...", file=sys.stderr)

            crawler = Crawler(
                engine_mode=engine_mode,
                selector_spec=analysis.selector_spec,
                output_dir=str(self.output_dir),
                max_workers=self.config.max_workers,
            )
            try:
                manifest = crawler.crawl(frontier)
            finally:
                crawler.close()

            manifest.start_url = self.config.start_url
            manifest.engine_mode = engine_mode.value

            # --- Quality check ---
            success_rate = manifest.total_pages / len(frontier) if frontier else 0
            print(f"  → Crawled {manifest.total_pages}/{len(frontier)} pages (success rate: {success_rate:.1%})", file=sys.stderr)

            if success_rate >= MIN_CRAWL_SUCCESS_RATE or attempt >= MAX_CRAWL_RETRIES:
                if success_rate < MIN_CRAWL_SUCCESS_RATE:
                    print(f"  [WARNING] Low success rate ({success_rate:.1%}) but max retries reached", file=sys.stderr)
                print(f"  → Final: {manifest.total_pages} pages into {manifest.total_files} files\n", file=sys.stderr)
                return manifest

            # --- Re-analyze with feedback ---
            print(f"  [QUALITY] Success rate {success_rate:.1%} < {MIN_CRAWL_SUCCESS_RATE:.0%} threshold — re-analyzing selectors...", file=sys.stderr)

            raw_dir = self.output_dir / "md" / "raw"
            if raw_dir.exists():
                shutil.rmtree(raw_dir)
                raw_dir.mkdir(parents=True, exist_ok=True)

            analysis = analyzer.reanalyze_selectors(
                start_url=self.config.start_url,
                base_url=base_url,
                start_html=start_html,
                previous_selector=analysis.selector_spec.content_selector,
                crawl_success_rate=success_rate,
                total_pages=len(frontier),
                sample_links=sample_links,
            )

            frontier = [r for r in full_frontier if analysis.scope_rules.url_matches(r.url)]
            if len(frontier) > self.config.max_pages:
                frontier = frontier[:self.config.max_pages]

            print(f"  → Re-filtered frontier: {len(frontier)} URLs", file=sys.stderr)
            print(f"  → New content selector: {analysis.selector_spec.content_selector}", file=sys.stderr)

            analysis_path = self.output_dir / "llm-analysis.json"
            analysis_path.write_text(analysis.model_dump_json(indent=2), encoding="utf-8")

        return manifest
