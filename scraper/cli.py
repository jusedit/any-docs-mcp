#!/usr/bin/env python3
"""CLI entry point for the AnyDocs scraper.

Usage:
    python cli.py scrape --url https://docs.example.com --name example-docs
    python cli.py scrape --url https://docs.example.com --name example-docs --output ./my-output
    python cli.py scrape --url https://docs.example.com --name example-docs --max-pages 200 --workers 5
"""
import os
import sys

import click
from colorama import Fore, init

from models import PipelineConfig
from pipeline import Pipeline

# Load .env from parent directory
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

init(autoreset=True)


@click.group()
def cli():
    """Scraper v2 — Deterministic Documentation Scraper + AGENTS.md Packager"""
    pass


@cli.command()
@click.option("--url", required=True, help="Start URL of documentation site")
@click.option("--name", required=True, help="Unique name for this documentation set")
@click.option("--output", default=None, help="Output directory (default: ./output/<name>)")
@click.option("--max-pages", default=500, help="Maximum pages to crawl (default: 500)")
@click.option("--workers", default=10, help="Concurrent workers for cURL mode (default: 10)")
@click.option("--threshold", default=0.3, type=float, help="Engine diff threshold (default: 0.3)")
@click.option("--analyzer-model", default="qwen/qwen3-coder-next", help="LLM model for analyzer")
def scrape(url, name, output, max_pages, workers, threshold, analyzer_model):
    """Scrape a documentation site and generate AGENTS.md package."""
    if not os.getenv("OPENROUTER_API_KEY"):
        print(f"{Fore.YELLOW}Warning: OPENROUTER_API_KEY not set. LLM features will use fallback heuristics.{Fore.RESET}")

    output_dir = output or os.path.join(".", "output", name)

    config = PipelineConfig(
        start_url=url,
        name=name,
        output_dir=output_dir,
        max_pages=max_pages,
        max_workers=workers,
        engine_diff_threshold=threshold,
        llm_model_analyzer=analyzer_model,
    )

    print(f"{Fore.CYAN}Starting scraper pipeline...{Fore.RESET}")
    print(f"  URL:        {url}")
    print(f"  Name:       {name}")
    print(f"  Output:     {output_dir}")
    print(f"  Max pages:  {max_pages}")
    print(f"  Workers:    {workers}")
    print()

    pipeline = Pipeline(config)
    agents_path = pipeline.run()

    print(f"\n{Fore.GREEN}Done!{Fore.RESET}")
    print(f"  AGENTS.md:  {agents_path}")
    print(f"  Raw MD:     {os.path.join(output_dir, 'md', 'raw')}")
    print(f"  Grouped MD: {os.path.join(output_dir, 'md', 'grouped')}")
    print(f"  Manifest:   {os.path.join(output_dir, 'manifest.json')}")


@cli.command()
@click.option("--url", required=True, help="URL to test engine selection on")
@click.option("--threshold", default=0.3, type=float, help="Diff threshold (default: 0.3)")
def test_engine(url, threshold):
    """Test engine selection (cURL vs Selenium) for a URL without full scrape."""
    from engine_selector import select_engine

    print(f"{Fore.CYAN}Testing engine selection for: {url}{Fore.RESET}\n")
    decision = select_engine(url, threshold=threshold)

    print(f"\n{Fore.GREEN}Result:{Fore.RESET}")
    print(f"  Engine:           {decision.mode.value}")
    print(f"  cURL MD length:   {decision.curl_md_length}")
    print(f"  Selenium MD len:  {decision.selenium_md_length}")
    print(f"  cURL headings:    {decision.curl_headings}")
    print(f"  Selenium headings:{decision.selenium_headings}")
    print(f"  cURL code blocks: {decision.curl_code_blocks}")
    print(f"  Selenium code:    {decision.selenium_code_blocks}")
    print(f"  Diff ratio:       {decision.diff_ratio:.2%}")
    print(f"  Reason:           {decision.reason}")


@cli.command()
@click.option("--url", required=True, help="URL to test discovery on")
@click.option("--sample-pages", default=10, help="Number of pages to sample (default: 10)")
def test_discovery(url, sample_pages):
    """Test URL discovery for a site without full scrape."""
    from discovery import DiscoveryWorker

    print(f"{Fore.CYAN}Testing discovery for: {url}{Fore.RESET}\n")
    worker = DiscoveryWorker()
    frontier, start_html, sample_links = worker.discover(url, max_sample_pages=sample_pages)

    print(f"\n{Fore.GREEN}Result:{Fore.RESET}")
    print(f"  Frontier URLs: {len(frontier)}")
    print(f"  Sample links:  {len(sample_links)}")
    print(f"\n  First 20 frontier URLs:")
    for rec in frontier[:20]:
        print(f"    [{rec.source}] {rec.url}")
    if len(frontier) > 20:
        print(f"    ... and {len(frontier) - 20} more")


if __name__ == "__main__":
    cli()
