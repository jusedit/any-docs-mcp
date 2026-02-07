"""
Batch scrape all 50 README sites using the new URL discovery.
Then run coverage audit.
"""
import subprocess
import sys
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

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


def scrape_site(name: str, url: str, max_pages: int = 300) -> dict:
    """Scrape a single site using the CLI."""
    # Use cli.py add command
    cmd = [
        sys.executable, "cli.py", "add",
        "--url", url,
        "--name", name,
        "--workers", "5",  # Conservative to avoid overwhelming servers
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
                # Extract "Scraped X pages"
                try:
                    parts = line.split()
                    for i, p in enumerate(parts):
                        if p.isdigit() and i > 0 and "scraped" in parts[i-1].lower():
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
            "output": output[-500:],  # Last 500 chars
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


def main():
    """Scrape all README sites sequentially (to avoid overwhelming servers)."""
    print(f"Batch scraping {len(README_SITES)} README sites...")
    print("This will take approximately 1-2 hours. Press Ctrl+C to cancel.\n")

    results = []
    success_count = 0

    for i, (name, url) in enumerate(README_SITES.items(), 1):
        print(f"[{i}/{len(README_SITES)}] Scraping {name} ({url})...")
        result = scrape_site(name, url, max_pages=300)
        results.append(result)

        if result["success"]:
            success_count += 1
            print(f"  ✓ Success: {result['pages_found']} pages in {result['elapsed']}s")
        else:
            print(f"  ✗ Failed: {result['output'][:200]}")

    # Save results
    output_file = Path(__file__).parent / "batch_scrape_results.json"
    with open(output_file, "w") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total": len(results),
            "success": success_count,
            "failed": len(results) - success_count,
            "results": results,
        }, f, indent=2)

    print(f"\n{'='*60}")
    print(f"Batch scrape complete: {success_count}/{len(results)} sites")
    print(f"Results saved to: {output_file}")

    # Now run coverage audit
    print(f"\n{'='*60}")
    print("Running coverage audit...")
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
