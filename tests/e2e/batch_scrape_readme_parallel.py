"""
Batch scrape all 50 README sites using the new URL discovery - PARALLEL VERSION.

Usage:
  python batch_scrape_readme_parallel.py
  python batch_scrape_readme_parallel.py --max-workers 8
  python batch_scrape_readme_parallel.py --sites react,nextjs,vuejs
"""
import argparse
import subprocess
import sys
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import threading
from datetime import datetime

# README sites from audit_url_coverage.py
README_SITES = {
    "python3": "https://docs.python.org/3/",
    "nodejs": "https://nodejs.org/api/",
    "typescript": "https://www.typescriptlang.org/docs/",
    "java": "https://docs.oracle.com/en/java/javase/",
    "kotlin": "https://kotlinlang.org/docs/home.html",
    "rust-book": "https://doc.rust-lang.org/book/",
    "golang": "https://go.dev/doc/",
    "dotnet": "https://learn.microsoft.com/en-us/dotnet/",
    "git": "https://git-scm.com/docs",
    "linux-man": "https://man7.org/linux/man-pages/",
    "swagger": "https://swagger.io/docs/",
    "grpc": "https://grpc.io/docs/",
    "webpack": "https://webpack.js.org/concepts/",
    "eslint": "https://eslint.org/docs/latest/",
    "vite": "https://vite.dev/guide/",
    "tailwind": "https://tailwindcss.com/docs",
    "react": "https://react.dev/",
    "nextjs": "https://nextjs.org/docs",
    "vuejs": "https://vuejs.org/guide/",
    "nuxt": "https://nuxt.com/docs",
    "angular": "https://angular.dev/",
    "svelte": "https://svelte.dev/docs",
    "sveltekit": "https://svelte.dev/docs/kit",
    "hyperapp": "https://github.com/jorgebucaran/hyperapp",
    "django": "https://docs.djangoproject.com/en/stable/",
    "flask": "https://flask.palletsprojects.com/en/stable/",
    "fastapi": "https://fastapi.tiangolo.com/",
    "rails": "https://guides.rubyonrails.org/",
    "laravel": "https://laravel.com/docs",
    "spring-boot": "https://docs.spring.io/spring-boot/reference/index.html",
    "postgresql": "https://www.postgresql.org/docs/current/",
    "mysql": "https://dev.mysql.com/doc/",
    "sqlite": "https://www.sqlite.org/docs.html",
    "redis": "https://redis.io/docs/latest/",
    "mongodb": "https://www.mongodb.com/docs/",
    "elasticsearch": "https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html",
    "kafka": "https://kafka.apache.org/documentation/",
    "rabbitmq": "https://www.rabbitmq.com/docs",
    "docker": "https://docs.docker.com/",
    "kubernetes": "https://kubernetes.io/docs/",
    "helm": "https://helm.sh/docs/",
    "terraform": "https://developer.hashicorp.com/terraform/docs",
    "ansible": "https://docs.ansible.com/ansible/latest/",
    "nginx": "https://nginx.org/en/docs/",
    "github": "https://docs.github.com/en",
    "aws": "https://docs.aws.amazon.com/",
    "gcloud": "https://docs.cloud.google.com/docs",
    "azure": "https://learn.microsoft.com/en-us/azure/",
    "openai": "https://platform.openai.com/docs/overview",
    "stripe": "https://docs.stripe.com/",
    "twilio": "https://www.twilio.com/docs",
}

# Thread-safe counters
lock = threading.Lock()
completed_count = 0
success_count = 0
failed_sites = []


def scrape_site(name: str, url: str, max_pages: int = 300) -> dict:
    """Scrape a single site using the CLI."""
    cmd = [
        sys.executable, "cli.py", "add",
        "--url", url,
        "--name", name,
        "--workers", "3",  # Lower per-site workers for parallel safety
    ]

    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            cwd=Path(__file__).parent.parent.parent / "scraper",
            capture_output=True,
            text=True,
            timeout=900,  # 15 minutes per site
        )
        elapsed = time.time() - start

        success = result.returncode == 0
        output = result.stdout + result.stderr

        # Parse pages from output
        pages_found = 0
        for line in output.split("\n"):
            if "pages into" in line.lower():
                try:
                    parts = line.split()
                    for i, p in enumerate(parts):
                        if p.isdigit() and i > 0 and parts[i-1].lower() in ["scraped", "done!"]:
                            pages_found = int(p)
                            break
                except:
                    pass

        return {
            "name": name,
            "url": url,
            "success": success,
            "pages_found": pages_found,
            "elapsed": round(elapsed, 1),
            "output": output[-500:],
        }
    except subprocess.TimeoutExpired:
        return {
            "name": name,
            "url": url,
            "success": False,
            "pages_found": 0,
            "elapsed": 900,
            "output": "TIMEOUT after 15 minutes",
        }
    except Exception as e:
        return {
            "name": name,
            "url": url,
            "success": False,
            "pages_found": 0,
            "elapsed": 0,
            "output": str(e),
        }


def scrape_with_progress(name: str, url: str, max_pages: int, total: int) -> dict:
    """Scrape with progress tracking."""
    global completed_count, success_count, failed_sites

    result = scrape_site(name, url, max_pages)

    with lock:
        completed_count += 1
        if result["success"]:
            success_count += 1
        else:
            failed_sites.append(name)

        status = "✓" if result["success"] else "✗"
        pages = result["pages_found"] if result["success"] else 0
        print(f"[{completed_count}/{total}] {status} {name}: {pages} pages ({result['elapsed']}s)")

    return result


def main():
    parser = argparse.ArgumentParser(description="Batch scrape README sites in parallel")
    parser.add_argument("--max-workers", type=int, default=6, help="Concurrent workers (default: 6)")
    parser.add_argument("--sites", help="Comma-separated list of sites to scrape (default: all)")
    parser.add_argument("--skip-existing", action="store_true", help="Skip sites already in AppData")
    args = parser.parse_args()

    # Filter sites if specified
    if args.sites:
        site_list = args.sites.split(",")
        sites_to_scrape = {k: v for k, v in README_SITES.items() if k in site_list}
    else:
        sites_to_scrape = README_SITES

    # Check for existing sites if --skip-existing
    if args.skip_existing:
        import os
        appdata = Path(os.environ.get("APPDATA", "")) / "AnyDocsMCP" / "docs"
        existing = set()
        if appdata.exists():
            existing = {d.name for d in appdata.iterdir() if d.is_dir()}
        sites_to_scrape = {k: v for k, v in sites_to_scrape.items() if k not in existing}
        print(f"Skipping {len(existing)} existing sites")

    total = len(sites_to_scrape)
    if total == 0:
        print("No sites to scrape!")
        return

    print(f"Batch scraping {total} README sites with {args.max_workers} workers...")
    print(f"Estimated time: {total * 3 // args.max_workers}-{total * 5 // args.max_workers} minutes\n")

    start_time = time.time()
    results = []

    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(scrape_with_progress, name, url, 300, total): name
            for name, url in sites_to_scrape.items()
        }

        # Collect results as they complete
        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    # Summary
    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"Batch scrape complete: {success_count}/{total} sites in {elapsed/60:.1f} minutes")

    if failed_sites:
        print(f"\nFailed sites ({len(failed_sites)}): {', '.join(failed_sites)}")

    # Save results
    output_file = Path(__file__).parent / f"batch_scrape_results_{datetime.now():%Y%m%d_%H%M%S}.json"
    with open(output_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total": len(results),
            "success": success_count,
            "failed": len(results) - success_count,
            "elapsed_minutes": round(elapsed / 60, 1),
            "failed_sites": failed_sites,
            "results": results,
        }, f, indent=2)
    print(f"Results saved to: {output_file}")

    # Now run coverage audit
    print(f"\n{'='*60}")
    print("Running coverage audit (quick mode)...")
    audit_cmd = [
        sys.executable,
        str(Path(__file__).parent / "audit_url_coverage.py"),
        "--all",
        "--max-pages", "200",
        "--quick",
    ]
    subprocess.run(audit_cmd)


if __name__ == "__main__":
    main()
