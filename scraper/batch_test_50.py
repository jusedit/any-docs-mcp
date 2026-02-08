#!/usr/bin/env python3
"""Batch test: scrape all 50 verified documentation sites with unlimited pages.

Usage:
    python batch_test_50.py [--start-from N] [--only NAME]

Results are written to batch_test_results.json as each site completes.
"""
import json
import os
import sys
import time
import traceback
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from models import PipelineConfig
from pipeline import Pipeline

# Load .env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

STORAGE_ROOT = os.environ.get(
    "ANYDOCS_STORAGE_ROOT",
    os.path.join(os.environ.get("APPDATA", ""), "AnyDocsMCP", "v2"),
)

SITES = [
    # Programming Languages
    ("python3", "https://docs.python.org/3/"),
    ("nodejs", "https://nodejs.org/api/"),
    ("typescript", "https://www.typescriptlang.org/docs/"),
    ("java-se", "https://docs.oracle.com/en/java/javase/"),
    ("kotlin", "https://kotlinlang.org/docs/home.html"),
    ("rust-book", "https://doc.rust-lang.org/book/"),
    ("golang", "https://go.dev/doc/"),
    ("dotnet", "https://learn.microsoft.com/en-us/dotnet/"),
    # Tools & Build Systems
    ("git", "https://git-scm.com/docs"),
    ("linux-man", "https://man7.org/linux/man-pages/"),
    ("swagger", "https://swagger.io/docs/"),
    ("grpc", "https://grpc.io/docs/"),
    ("webpack", "https://webpack.js.org/concepts/"),
    ("eslint", "https://eslint.org/docs/latest/"),
    ("vite", "https://vite.dev/guide/"),
    ("tailwind", "https://tailwindcss.com/docs"),
    # Web Frameworks (Frontend)
    ("react", "https://react.dev/"),
    ("nextjs", "https://nextjs.org/docs"),
    ("vuejs", "https://vuejs.org/guide/"),
    ("nuxt", "https://nuxt.com/docs"),
    ("angular", "https://angular.dev/"),
    ("svelte", "https://svelte.dev/docs"),
    ("sveltekit", "https://svelte.dev/docs/kit"),
    ("hyperapp", "https://github.com/jorgebucaran/hyperapp"),
    # Web Frameworks (Backend)
    #("django", "https://docs.djangoproject.com/en/stable/"),
    ("flask", "https://flask.palletsprojects.com/en/stable/"),
    ("fastapi", "https://fastapi.tiangolo.com/"),
    ("rails", "https://guides.rubyonrails.org/"),
    ("laravel", "https://laravel.com/docs"),
    ("spring-boot", "https://docs.spring.io/spring-boot/reference/index.html"),
    # Databases
    ("postgresql", "https://www.postgresql.org/docs/current/"),
    ("mysql", "https://dev.mysql.com/doc/"),
    ("sqlite", "https://www.sqlite.org/docs.html"),
    #("redis", "https://redis.io/docs/latest/"),
    ("mongodb", "https://www.mongodb.com/docs/"),
    ("elasticsearch", "https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html"),
    # Message Queues & Streaming
    ("kafka", "https://kafka.apache.org/documentation/"),
    ("rabbitmq", "https://www.rabbitmq.com/docs"),
    # DevOps & Infrastructure
    ("docker", "https://docs.docker.com/"),
    ("kubernetes", "https://kubernetes.io/docs/"),
    ("helm", "https://helm.sh/docs/"),
    ("terraform", "https://developer.hashicorp.com/terraform/docs"),
    ("ansible", "https://docs.ansible.com/ansible/latest/"),
    ("nginx", "https://nginx.org/en/docs/"),
    # Cloud Providers & APIs
    ("github-docs", "https://docs.github.com/en"),
    ("aws", "https://docs.aws.amazon.com/"),
    ("gcloud", "https://docs.cloud.google.com/docs"),
    ("azure", "https://learn.microsoft.com/en-us/azure/"),
    ("openai", "https://platform.openai.com/docs/overview"),
    ("stripe", "https://docs.stripe.com/"),
    ("twilio", "https://www.twilio.com/docs"),
]

RESULTS_FILE = Path(__file__).parent / "batch_test_results.json"


def load_results():
    if RESULTS_FILE.exists():
        return json.loads(RESULTS_FILE.read_text(encoding="utf-8"))
    return {}


def save_results(results):
    RESULTS_FILE.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")


def run_site(name: str, url: str, max_pages: int = 2000) -> dict:
    """Run the scraper pipeline for a single site. Returns result dict."""
    output_dir = os.path.join(STORAGE_ROOT, name)
    config = PipelineConfig(
        start_url=url,
        name=name,
        output_dir=output_dir,
        max_pages=max_pages,
        max_workers=10,
        llm_model_analyzer="qwen/qwen3-coder-next",
    )

    start = time.time()
    try:
        pipeline = Pipeline(config)
        agents_path = pipeline.run()
        elapsed = time.time() - start

        # Read manifest for stats
        manifest_path = Path(output_dir) / "manifest.json"
        pages = 0
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            pages = manifest.get("total_pages", 0)

        agents_size = agents_path.stat().st_size if agents_path.exists() else 0

        return {
            "status": "success",
            "pages": pages,
            "agents_md_bytes": agents_size,
            "elapsed_s": round(elapsed, 1),
            "error": None,
        }
    except Exception as e:
        elapsed = time.time() - start
        return {
            "status": "error",
            "pages": 0,
            "agents_md_bytes": 0,
            "elapsed_s": round(elapsed, 1),
            "error": f"{type(e).__name__}: {e}",
            "traceback": traceback.format_exc(),
        }


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-from", type=int, default=0, help="Start from site index N (0-based)")
    parser.add_argument("--only", type=str, default=None, help="Only run a specific site by name")
    args = parser.parse_args()

    results = load_results()

    sites = SITES
    if args.only:
        sites = [(n, u) for n, u in SITES if n == args.only]
        if not sites:
            print(f"Site '{args.only}' not found in list")
            sys.exit(1)

    total = len(sites)
    start_idx = args.start_from

    print(f"\n{'='*70}")
    print(f"  BATCH TEST: {total} documentation sites (unlimited pages)")
    print(f"  Starting from index: {start_idx}")
    print(f"  Results: {RESULTS_FILE}")
    print(f"{'='*70}\n")

    for i, (name, url) in enumerate(sites):
        if i < start_idx:
            continue

        # Skip if already succeeded
        if name in results and results[name].get("status") == "success":
            print(f"[{i+1}/{total}] {name} — SKIPPED (already succeeded: {results[name]['pages']} pages)")
            continue

        print(f"\n{'─'*70}")
        print(f"[{i+1}/{total}] {name}")
        print(f"  URL: {url}")
        print(f"{'─'*70}")

        result = run_site(name, url)
        results[name] = result
        save_results(results)

        if result["status"] == "success":
            print(f"\n  ✓ {name}: {result['pages']} pages, {result['agents_md_bytes']}B index, {result['elapsed_s']}s")
        else:
            print(f"\n  ✗ {name}: FAILED — {result['error']}")

    # Summary
    print(f"\n\n{'='*70}")
    print(f"  SUMMARY")
    print(f"{'='*70}")
    succeeded = [n for n, r in results.items() if r.get("status") == "success"]
    failed = [n for n, r in results.items() if r.get("status") == "error"]
    print(f"  Succeeded: {len(succeeded)}/{len(results)}")
    print(f"  Failed:    {len(failed)}")
    if failed:
        print(f"\n  Failed sites:")
        for name in failed:
            print(f"    - {name}: {results[name].get('error', 'unknown')}")
    total_pages = sum(r.get("pages", 0) for r in results.values())
    print(f"\n  Total pages scraped: {total_pages}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
