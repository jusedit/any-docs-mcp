#!/usr/bin/env python3
import click
from datetime import datetime
from colorama import init, Fore
from site_analyzer import SiteAnalyzer
from scraper_engine import ScraperEngine
from storage import StorageManager
from models import DocumentationConfig

init(autoreset=True)
storage = StorageManager()


@click.group()
def cli():
    """AnyDocsMCP - Universal Documentation Scraper"""
    pass


@cli.command()
@click.option('--url', required=True, help='Start URL of documentation')
@click.option('--name', required=True, help='Unique name for this documentation set')
@click.option('--display-name', help='Display name (defaults to name)')
def add(url, name, display_name):
    """Add a new documentation site"""
    print(f"{Fore.CYAN}Analyzing {url}...{Fore.RESET}")
    
    analyzer = SiteAnalyzer()
    analysis = analyzer.analyze_site(url)
    
    print(f"{Fore.GREEN}Analysis complete!{Fore.RESET}")
    print(f"Content selectors: {analysis.content_selectors}")
    print(f"Navigation selectors: {analysis.navigation_selectors}")
    
    config = DocumentationConfig(
        name=name,
        display_name=display_name or name,
        start_url=url,
        site_analysis=analysis,
        version='v1',
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    storage.save_config(config)
    version = storage.create_version(name)
    
    print(f"{Fore.CYAN}Starting scrape...{Fore.RESET}")
    engine = ScraperEngine(config, storage)
    page_counts = engine.scrape_all(version)
    
    metadata = {
        'total_pages': sum(page_counts.values()),
        'total_files': len(page_counts),
        'last_scraped': datetime.now().isoformat()
    }
    storage.save_metadata(name, metadata)
    
    print(f"{Fore.GREEN}Done! Scraped {metadata['total_pages']} pages into {metadata['total_files']} files{Fore.RESET}")


@cli.command()
@click.option('--name', required=True, help='Documentation set name')
def update(name):
    """Re-scrape documentation"""
    config = storage.load_config(name)
    if not config:
        print(f"{Fore.RED}Documentation '{name}' not found{Fore.RESET}")
        return
    
    version = storage.create_version(name)
    config.version = version
    config.updated_at = datetime.now().isoformat()
    storage.save_config(config)
    
    print(f"{Fore.CYAN}Re-scraping {config.display_name}...{Fore.RESET}")
    engine = ScraperEngine(config, storage)
    page_counts = engine.scrape_all(version)
    
    metadata = storage.load_metadata(name)
    metadata.update({
        'total_pages': sum(page_counts.values()),
        'total_files': len(page_counts),
        'last_scraped': datetime.now().isoformat()
    })
    storage.save_metadata(name, metadata)
    
    print(f"{Fore.GREEN}Done!{Fore.RESET}")


@cli.command()
def list():
    """List all documentation sets"""
    docs = storage.list_documentation_sets()
    
    if not docs:
        print(f"{Fore.YELLOW}No documentation sets found{Fore.RESET}")
        return
    
    print(f"{Fore.CYAN}Documentation Sets:{Fore.RESET}\n")
    for doc_name in docs:
        config = storage.load_config(doc_name)
        metadata = storage.load_metadata(doc_name)
        
        print(f"{Fore.GREEN}• {doc_name}{Fore.RESET}")
        if config:
            print(f"  Display: {config.display_name}")
            print(f"  URL: {config.start_url}")
            print(f"  Version: {storage.get_latest_version(doc_name)}")
        if metadata:
            print(f"  Pages: {metadata.get('total_pages', 'N/A')}")
            print(f"  Files: {metadata.get('total_files', 'N/A')}")
        print()


if __name__ == '__main__':
    cli()
