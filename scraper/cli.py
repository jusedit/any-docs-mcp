#!/usr/bin/env python3
import click
import json
import os
from datetime import datetime, timedelta
from colorama import init, Fore
from site_analyzer import SiteAnalyzer
from scraper_engine import ScraperEngine
from storage import StorageManager
from models import DocumentationConfig

DEFAULT_REFRESH_DAYS = int(os.getenv('ANYDOCS_REFRESH_DAYS', '30'))

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


@cli.command()
@click.option('--url', required=True, help='Start URL of documentation')
@click.option('--name', required=True, help='Unique name for this documentation set')
@click.option('--display-name', help='Display name (defaults to name)')
@click.option('--json-progress', is_flag=True, help='Output progress as JSON for programmatic use')
@click.option('--workers', default=10, help='Number of concurrent workers (default: 10)')
def add(url, name, display_name, json_progress, workers):
    """Add a new documentation site"""
    if json_progress:
        print(f'PROGRESS:{{"phase":"analyzing","message":"Analyzing {url}..."}}', flush=True)
    else:
        print(f"{Fore.CYAN}Analyzing {url}...{Fore.RESET}")
    
    analyzer = SiteAnalyzer()
    analysis = analyzer.analyze_site(url)
    
    if not json_progress:
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
    
    if not json_progress:
        print(f"{Fore.CYAN}Starting scrape...{Fore.RESET}")
    
    engine = ScraperEngine(config, storage, max_workers=workers, json_progress=json_progress)
    page_counts = engine.scrape_all(version)
    
    content_hash = engine.get_combined_hash()
    refresh_after = (datetime.now() + timedelta(days=DEFAULT_REFRESH_DAYS)).isoformat()
    
    metadata = {
        'total_pages': sum(page_counts.values()),
        'total_files': len(page_counts),
        'last_scraped': datetime.now().isoformat(),
        'content_hash': content_hash,
        'refresh_after': refresh_after
    }
    storage.save_metadata(name, metadata)
    
    config.content_hash = content_hash
    storage.save_config(config)
    
    if json_progress:
        result = {
            'phase': 'completed',
            'message': f'Scraped {metadata["total_pages"]} pages into {metadata["total_files"]} files',
            'result': {
                'total_pages': metadata['total_pages'],
                'total_files': metadata['total_files'],
                'version': version,
                'content_hash': content_hash
            }
        }
        print(f'PROGRESS:{json.dumps(result)}', flush=True)
    else:
        print(f"{Fore.GREEN}Done! Scraped {metadata['total_pages']} pages into {metadata['total_files']} files{Fore.RESET}")


@cli.command()
@click.option('--name', required=True, help='Documentation set name')
@click.option('--json-progress', is_flag=True, help='Output progress as JSON for programmatic use')
@click.option('--force', is_flag=True, help='Force update even if content has not changed')
@click.option('--workers', default=10, help='Number of concurrent workers (default: 10)')
def update(name, json_progress, force, workers):
    """Re-scrape documentation"""
    config = storage.load_config(name)
    if not config:
        if json_progress:
            print(f'PROGRESS:{{"phase":"failed","message":"Documentation \'{name}\' not found"}}', flush=True)
        else:
            print(f"{Fore.RED}Documentation '{name}' not found{Fore.RESET}")
        sys.exit(1)
    
    old_metadata = storage.load_metadata(name)
    old_hash = old_metadata.get('content_hash')
    
    version = storage.create_version(name)
    config.version = version
    config.updated_at = datetime.now().isoformat()
    storage.save_config(config)
    
    if not json_progress:
        print(f"{Fore.CYAN}Re-scraping {config.display_name}...{Fore.RESET}")
    
    engine = ScraperEngine(config, storage, max_workers=workers, json_progress=json_progress)
    page_counts = engine.scrape_all(version)
    
    new_hash = engine.get_combined_hash()
    refresh_after = (datetime.now() + timedelta(days=DEFAULT_REFRESH_DAYS)).isoformat()
    
    content_changed = old_hash != new_hash if old_hash else True
    
    metadata = storage.load_metadata(name)
    metadata.update({
        'total_pages': sum(page_counts.values()),
        'total_files': len(page_counts),
        'last_scraped': datetime.now().isoformat(),
        'content_hash': new_hash,
        'refresh_after': refresh_after,
        'content_changed': content_changed
    })
    storage.save_metadata(name, metadata)
    
    config.content_hash = new_hash
    storage.save_config(config)
    
    if json_progress:
        result = {
            'phase': 'completed',
            'message': f'Scraped {metadata["total_pages"]} pages into {metadata["total_files"]} files',
            'result': {
                'total_pages': metadata['total_pages'],
                'total_files': metadata['total_files'],
                'version': version,
                'content_hash': new_hash,
                'content_changed': content_changed
            }
        }
        print(f'PROGRESS:{json.dumps(result)}', flush=True)
    else:
        change_msg = "Content changed!" if content_changed else "No content changes detected."
        print(f"{Fore.GREEN}Done! {change_msg}{Fore.RESET}")


@cli.command()
@click.option('--json', 'json_output', is_flag=True, help='Output as JSON')
def list(json_output):
    """List all documentation sets"""
    docs = storage.list_documentation_sets()
    
    if json_output:
        result = []
        for doc_name in docs:
            config = storage.load_config(doc_name)
            metadata = storage.load_metadata(doc_name)
            
            refresh_after = metadata.get('refresh_after') if metadata else None
            needs_refresh = False
            if refresh_after:
                try:
                    needs_refresh = datetime.fromisoformat(refresh_after) < datetime.now()
                except:
                    pass
            
            doc_info = {
                'name': doc_name,
                'display_name': config.display_name if config else doc_name,
                'url': config.start_url if config else None,
                'version': storage.get_latest_version(doc_name),
                'total_pages': metadata.get('total_pages') if metadata else None,
                'total_files': metadata.get('total_files') if metadata else None,
                'last_scraped': metadata.get('last_scraped') if metadata else None,
                'content_hash': metadata.get('content_hash') if metadata else None,
                'refresh_after': refresh_after,
                'needs_refresh': needs_refresh
            }
            result.append(doc_info)
        print(json.dumps(result, indent=2))
        return
    
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
            print(f"  Last Scraped: {metadata.get('last_scraped', 'N/A')}")
            if metadata.get('content_hash'):
                print(f"  Content Hash: {metadata.get('content_hash')[:12]}...")
            if metadata.get('refresh_after'):
                refresh_after = metadata.get('refresh_after')
                try:
                    needs_refresh = datetime.fromisoformat(refresh_after) < datetime.now()
                    status = f"{Fore.RED}NEEDS REFRESH{Fore.RESET}" if needs_refresh else f"{Fore.GREEN}OK{Fore.RESET}"
                    print(f"  Refresh After: {refresh_after[:10]} ({status})")
                except:
                    print(f"  Refresh After: {refresh_after}")
        print()


@cli.command()
@click.option('--name', required=True, help='Documentation set name')
@click.option('--json', 'json_output', is_flag=True, help='Output as JSON')
def check_update(name, json_output):
    """Check if documentation needs update (based on refresh timeout)"""
    config = storage.load_config(name)
    if not config:
        if json_output:
            print(json.dumps({'error': f"Documentation '{name}' not found", 'needs_update': False}))
        else:
            print(f"{Fore.RED}Documentation '{name}' not found{Fore.RESET}")
        sys.exit(1)
    
    metadata = storage.load_metadata(name)
    refresh_after = metadata.get('refresh_after') if metadata else None
    last_scraped = metadata.get('last_scraped') if metadata else None
    
    needs_update = False
    reason = None
    
    if not last_scraped:
        needs_update = True
        reason = 'Never scraped'
    elif refresh_after:
        try:
            if datetime.fromisoformat(refresh_after) < datetime.now():
                needs_update = True
                reason = f'Refresh timeout exceeded (was {refresh_after[:10]})'
        except:
            pass
    
    if json_output:
        print(json.dumps({
            'name': name,
            'needs_update': needs_update,
            'reason': reason,
            'last_scraped': last_scraped,
            'refresh_after': refresh_after,
            'content_hash': metadata.get('content_hash') if metadata else None
        }))
    else:
        if needs_update:
            print(f"{Fore.YELLOW}Documentation '{name}' needs update: {reason}{Fore.RESET}")
        else:
            print(f"{Fore.GREEN}Documentation '{name}' is up to date{Fore.RESET}")
            if last_scraped:
                print(f"  Last scraped: {last_scraped}")
            if refresh_after:
                print(f"  Next refresh: {refresh_after[:10]}")


if __name__ == '__main__':
    cli()
