"""Mock HTTP server that replays captured responses for testing."""
import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from pathlib import Path
from typing import Dict, Any, Optional
import threading


class FixtureRequestHandler(BaseHTTPRequestHandler):
    """Handler that serves captured fixture files."""
    
    # Class-level fixtures directory
    fixtures_dir: Path = None
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass
    
    def do_GET(self):
        """Handle GET request by serving fixture."""
        try:
            fixture = self._lookup_fixture()
            if fixture:
                self._serve_fixture(fixture)
            else:
                self._serve_404()
        except Exception as e:
            self._serve_500(str(e))
    
    def _lookup_fixture(self) -> Optional[Dict[str, Any]]:
        """Find matching fixture for current path."""
        # Path format: /{doc-name}/{path-to-slug}
        path_parts = self.path.strip('/').split('/')
        if len(path_parts) < 1:
            return None
        
        doc_name = path_parts[0]
        slug = '-'.join(path_parts[1:]) if len(path_parts) > 1 else 'index'
        
        # Look for fixture files
        doc_dir = self.fixtures_dir / doc_name
        if not doc_dir.exists():
            return None
        
        # Try exact match first
        meta_path = doc_dir / f"{slug}.meta.json"
        body_path = doc_dir / f"{slug}.body.html"
        
        if meta_path.exists() and body_path.exists():
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            with open(body_path, 'r', encoding='utf-8') as f:
                body = f.read()
            return {"meta": meta, "body": body}
        
        # Try to find any matching slug (for collision cases with hash suffix)
        for meta_file in doc_dir.glob("*.meta.json"):
            file_slug = meta_file.stem.replace('.meta', '')
            if file_slug.startswith(slug):
                body_file = meta_file.with_suffix('').with_suffix('.body.html')
                if body_file.exists():
                    with open(meta_file, 'r', encoding='utf-8') as f:
                        meta = json.load(f)
                    with open(body_file, 'r', encoding='utf-8') as f:
                        body = f.read()
                    return {"meta": meta, "body": body}
        
        return None
    
    def _serve_fixture(self, fixture: Dict[str, Any]):
        """Serve successful fixture response."""
        meta = fixture["meta"]
        body = fixture["body"].encode('utf-8')
        
        self.send_response(meta.get("status", 200))
        
        # Send headers from fixture
        headers = meta.get("headers", {})
        content_type_sent = False
        for key, value in headers.items():
            if key.lower() not in ['content-length', 'transfer-encoding']:
                self.send_header(key, value)
                if key.lower() == 'content-type':
                    content_type_sent = True
        
        # Ensure content-type is set
        if not content_type_sent:
            self.send_header('Content-Type', 'text/html; charset=utf-8')
        
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)
    
    def _serve_404(self):
        """Serve 404 response."""
        body = b"Fixture not found"
        self.send_response(404)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)
    
    def _serve_500(self, message: str):
        """Serve 500 response."""
        body = f"Server error: {message}".encode('utf-8')
        self.send_response(500)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """HTTP server that handles concurrent requests."""
    daemon_threads = True
    allow_reuse_address = True


class FixtureHTTPServer:
    """Mock server that replays captured HTTP responses."""
    
    def __init__(self, fixtures_dir: str = "tests/fixtures/real-world"):
        self.fixtures_dir = Path(fixtures_dir)
        self.server: Optional[ThreadedHTTPServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self.port: Optional[int] = None
        self.base_url: Optional[str] = None
    
    def start(self, port: int = 0) -> str:
        """Start server on random or specified port. Returns base URL."""
        # Ensure fixtures dir exists
        self.fixtures_dir.mkdir(parents=True, exist_ok=True)
        
        # Create handler class with fixtures directory
        handler = type('FixedHandler', (FixtureRequestHandler,), {
            'fixtures_dir': self.fixtures_dir
        })
        
        # Start server
        self.server = ThreadedHTTPServer(('localhost', port), handler)
        self.port = self.server.server_address[1]
        self.base_url = f"http://localhost:{self.port}"
        
        # Run in thread
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        return self.base_url
    
    def stop(self):
        """Stop the server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
            self.server_thread = None
    
    def get_rewritten_url(self, original_url: str) -> str:
        """Rewrite original URL to point to this server.
        
        Example:
            https://react.dev/learn/state → http://localhost:{port}/react/learn-state
        """
        if not self.base_url:
            raise RuntimeError("Server not started")
        
        # Remove protocol and get path
        url = re.sub(r'^https?://', '', original_url)
        
        # Extract domain (first component only, not TLD)
        parts = url.split('/', 1)
        domain_parts = parts[0].split('.')
        # Use first meaningful part (react from react.dev, fastapi from fastapi.tiangolo.com)
        domain = domain_parts[0] if domain_parts[0] not in ['www', 'docs'] else (domain_parts[1] if len(domain_parts) > 1 else domain_parts[0])
        
        if len(parts) > 1 and parts[1]:
            path = parts[1].rstrip('/')
            # Convert path to slug format
            path_slug = re.sub(r'[^a-zA-Z0-9]', '-', path)
            path_slug = re.sub(r'-+', '-', path_slug).strip('-')
            return f"{self.base_url}/{domain}/{path_slug}"
        else:
            return f"{self.base_url}/{domain}/index"
