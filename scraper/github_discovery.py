"""
GitHub Repository Documentation Discovery.

Specialized handler for GitHub repositories with documentation.
Discovers markdown files in docs/, README.md, and other documentation files.
"""
import re
import requests
from typing import List, Dict, Optional
from urllib.parse import urlparse, urljoin


class GitHubDiscovery:
    """Discover documentation files in GitHub repositories."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'AnyDocsMCP/1.0'
        })
    
    @staticmethod
    def is_github_repo(url: str) -> bool:
        """Check if URL is a GitHub repository."""
        parsed = urlparse(url)
        if parsed.netloc not in ['github.com', 'www.github.com']:
            return False
        
        # Match pattern: github.com/owner/repo
        path_parts = [p for p in parsed.path.split('/') if p]
        return len(path_parts) >= 2
    
    def extract_repo_info(self, url: str) -> Optional[Dict[str, str]]:
        """
        Extract owner and repo from GitHub URL.
        
        Examples:
            https://github.com/jorgebucaran/hyperapp -> {owner: jorgebucaran, repo: hyperapp}
            https://github.com/user/repo/tree/main -> {owner: user, repo: repo, branch: main}
        """
        parsed = urlparse(url)
        path_parts = [p for p in parsed.path.split('/') if p]
        
        if len(path_parts) < 2:
            return None
        
        info = {
            'owner': path_parts[0],
            'repo': path_parts[1],
            'branch': 'main'  # Default
        }
        
        # Check for branch in URL: /tree/branch-name or /blob/branch-name
        if len(path_parts) >= 4 and path_parts[2] in ['tree', 'blob']:
            info['branch'] = path_parts[3]
        
        return info
    
    def discover_markdown_files(self, url: str, max_files: int = 100) -> List[Dict[str, str]]:
        """
        Discover all markdown files in a GitHub repository.
        
        Returns:
            [{'url': raw_url, 'title': filename, 'path': relative_path}]
        """
        repo_info = self.extract_repo_info(url)
        if not repo_info:
            print("  GitHub: Invalid repository URL")
            return []
        
        owner = repo_info['owner']
        repo = repo_info['repo']
        branch = repo_info['branch']
        
        print(f"  GitHub: Discovering docs in {owner}/{repo} (branch: {branch})")
        
        markdown_files = []
        
        # Try to get repository tree via GitHub API
        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        
        try:
            response = self.session.get(api_url, timeout=30)
            
            # If API rate limited or fails, try alternative method
            if response.status_code != 200:
                print(f"  GitHub API: Status {response.status_code}, trying alternative method")
                return self._discover_via_web_scraping(owner, repo, branch, max_files)
            
            data = response.json()
            
            if 'tree' not in data:
                print("  GitHub: No tree data in response")
                return []
            
            # Filter for markdown files
            for item in data['tree']:
                if item['type'] != 'blob':
                    continue
                
                path = item['path']
                
                # Include markdown files
                if not path.endswith('.md'):
                    continue
                
                # Prioritize docs/ folder and important files
                is_priority = (
                    path.startswith('docs/') or
                    path.startswith('documentation/') or
                    path == 'README.md' or
                    path.upper() == 'README.MD' or
                    'guide' in path.lower() or
                    'tutorial' in path.lower()
                )
                
                # Skip hidden folders and common excludes
                if any(part.startswith('.') for part in path.split('/')):
                    continue
                
                if any(exclude in path.lower() for exclude in [
                    'node_modules/', 'vendor/', '.github/', 'test/', 'tests/',
                    '__pycache__/', 'dist/', 'build/', 'coverage/'
                ]):
                    continue
                
                # Convert to raw GitHub URL
                raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
                
                # Extract title from path
                title = path.split('/')[-1].replace('.md', '').replace('-', ' ').replace('_', ' ').title()
                
                markdown_files.append({
                    'url': raw_url,
                    'title': title,
                    'path': path,
                    'priority': is_priority
                })
            
            # Sort: priority files first, then by path
            markdown_files.sort(key=lambda x: (not x['priority'], x['path']))
            
            # Limit results
            markdown_files = markdown_files[:max_files]
            
            print(f"  GitHub: Found {len(markdown_files)} markdown files")
            
            return markdown_files
            
        except Exception as e:
            print(f"  GitHub API error: {e}")
            return self._discover_via_web_scraping(owner, repo, branch, max_files)
    
    def _discover_via_web_scraping(self, owner: str, repo: str, branch: str, max_files: int) -> List[Dict[str, str]]:
        """
        Fallback: Discover docs via web scraping the GitHub UI.
        Looks for common documentation patterns.
        """
        print(f"  GitHub: Using web scraping fallback")
        
        markdown_files = []
        
        # Check common documentation paths
        common_paths = [
            'docs',
            'documentation',
            'doc',
            '',  # Root for README
        ]
        
        for path in common_paths:
            try:
                # Construct GitHub folder URL
                if path:
                    folder_url = f"https://github.com/{owner}/{repo}/tree/{branch}/{path}"
                else:
                    folder_url = f"https://github.com/{owner}/{repo}"
                
                response = self.session.get(folder_url, timeout=15)
                if response.status_code != 200:
                    continue
                
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find file links (.md files)
                for link in soup.find_all('a', href=True):
                    href = link.get('href', '')
                    
                    # Match pattern: /owner/repo/blob/branch/path/file.md
                    if f'/{owner}/{repo}/blob/' in href and href.endswith('.md'):
                        # Extract file path
                        parts = href.split(f'/{owner}/{repo}/blob/{branch}/')
                        if len(parts) < 2:
                            continue
                        
                        file_path = parts[1]
                        
                        # Convert to raw URL
                        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
                        
                        title = file_path.split('/')[-1].replace('.md', '').replace('-', ' ').replace('_', ' ').title()
                        
                        markdown_files.append({
                            'url': raw_url,
                            'title': title,
                            'path': file_path,
                            'priority': 'README' in file_path.upper() or path == 'docs'
                        })
                
            except Exception as e:
                print(f"  GitHub web scraping error for {path}: {e}")
                continue
        
        # Remove duplicates and limit
        seen_urls = set()
        unique_files = []
        for f in markdown_files:
            if f['url'] not in seen_urls:
                seen_urls.add(f['url'])
                unique_files.append(f)
        
        unique_files.sort(key=lambda x: (not x['priority'], x['path']))
        unique_files = unique_files[:max_files]
        
        print(f"  GitHub: Web scraping found {len(unique_files)} files")
        
        return unique_files
    
    def convert_blob_to_raw(self, url: str) -> str:
        """
        Convert GitHub blob URL to raw URL.
        
        Examples:
            https://github.com/user/repo/blob/main/docs/file.md
            -> https://raw.githubusercontent.com/user/repo/main/docs/file.md
        """
        if 'raw.githubusercontent.com' in url:
            return url
        
        # Pattern: github.com/owner/repo/blob/branch/path
        match = re.match(
            r'https?://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)',
            url
        )
        
        if match:
            owner, repo, branch, path = match.groups()
            return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
        
        return url
