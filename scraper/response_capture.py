"""HTTP Response capture system for real-world testing fixtures."""
import json
import re
import gzip
import hashlib
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import requests


@dataclass
class CapturedResponse:
    """Represents a captured HTTP response."""
    status: int
    headers: Dict[str, str]
    body: str
    url: str
    captured_at: str = ""
    
    def __post_init__(self):
        if not self.captured_at:
            self.captured_at = datetime.utcnow().isoformat() + "Z"


class ResponseCapture:
    """Captures HTTP responses and stores them as fixture files."""
    
    MAX_BODY_SIZE = 1024 * 1024  # 1 MB limit
    
    def __init__(self, fixtures_dir: str = "tests/fixtures/real-world"):
        self.fixtures_dir = Path(fixtures_dir)
        self.fixtures_dir.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def url_to_slug(url: str) -> str:
        """Convert URL to human-readable slug for filenames.
        
        Examples:
            https://react.dev/learn/state → react-dev-learn-state
            https://fastapi.tiangolo.com/tutorial/ → fastapi-tiangolo-com-tutorial
        """
        # Remove protocol
        url = re.sub(r'^https?://', '', url)
        # Remove query params and fragment
        url = url.split('?')[0].split('#')[0]
        # Replace non-alphanumeric with hyphens
        slug = re.sub(r'[^a-zA-Z0-9]', '-', url)
        # Collapse multiple hyphens
        slug = re.sub(r'-+', '-', slug)
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        # Limit length
        if len(slug) > 100:
            # Use hash for very long URLs
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            slug = slug[:80] + '-' + url_hash
        return slug.lower()
    
    def capture(self, url: str, timeout: int = 30) -> CapturedResponse:
        """Fetch URL and return CapturedResponse."""
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        # Truncate if too large
        body = response.text
        if len(body) > self.MAX_BODY_SIZE:
            body = body[:self.MAX_BODY_SIZE]
            
        return CapturedResponse(
            status=response.status_code,
            headers=dict(response.headers),
            body=body,
            url=url
        )
    
    def save(self, captured: CapturedResponse, doc_name: str, compress_threshold_kb: int = 100) -> tuple[Path, Path]:
        """Save captured response as .meta.json + .body.html[.gz] pair.
        
        Files larger than compress_threshold_kb are gzip compressed.
        """
        # Create doc directory
        doc_dir = self.fixtures_dir / doc_name
        doc_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate slug from URL
        slug = self.url_to_slug(captured.url)
        
        # Handle collisions by appending hash
        meta_path = doc_dir / f"{slug}.meta.json"
        body_path = doc_dir / f"{slug}.body.html"
        
        if meta_path.exists():
            # Append URL hash for uniqueness
            url_hash = hashlib.md5(captured.url.encode()).hexdigest()[:6]
            slug = f"{slug}-{url_hash}"
            meta_path = doc_dir / f"{slug}.meta.json"
            body_path = doc_dir / f"{slug}.body.html"
        
        # Determine if compression is needed
        body_bytes = captured.body.encode('utf-8')
        original_size = len(body_bytes)
        use_compression = original_size > (compress_threshold_kb * 1024)
        
        if use_compression:
            # Compress and use .gz extension
            body_path = doc_dir / f"{slug}.body.html.gz"
            compressed = gzip.compress(body_bytes)
            with open(body_path, 'wb') as f:
                f.write(compressed)
            compressed_size = len(compressed)
        else:
            # Write uncompressed
            with open(body_path, 'w', encoding='utf-8') as f:
                f.write(captured.body)
            compressed_size = original_size
        
        # Write metadata with compression info
        meta = {
            "status": captured.status,
            "headers": captured.headers,
            "original_url": captured.url,
            "captured_at": captured.captured_at,
            "slug": slug,
            "compression": {
                "enabled": use_compression,
                "original_size_bytes": original_size,
                "compressed_size_bytes": compressed_size,
                "savings_percent": round((1 - compressed_size/original_size) * 100, 1) if use_compression else 0
            }
        }
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2)
        
        return meta_path, body_path
    
    def load(self, doc_name: str, slug: str) -> CapturedResponse:
        """Load captured response from disk (handles both .html and .html.gz)."""
        doc_dir = self.fixtures_dir / doc_name
        
        with open(doc_dir / f"{slug}.meta.json", 'r', encoding='utf-8') as f:
            meta = json.load(f)
        
        # Check for compressed file first
        gz_path = doc_dir / f"{slug}.body.html.gz"
        html_path = doc_dir / f"{slug}.body.html"
        
        if gz_path.exists():
            with open(gz_path, 'rb') as f:
                body = gzip.decompress(f.read()).decode('utf-8')
        elif html_path.exists():
            with open(html_path, 'r', encoding='utf-8') as f:
                body = f.read()
        else:
            raise FileNotFoundError(f"No body file found for {slug}")
        
        return CapturedResponse(
            status=meta["status"],
            headers=meta["headers"],
            body=body,
            url=meta["original_url"],
            captured_at=meta.get("captured_at", "")
        )


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python -m response_capture capture <url> <doc-name>")
        sys.exit(1)
    
    if sys.argv[1] == "capture":
        url = sys.argv[2]
        doc_name = sys.argv[3] if len(sys.argv) > 3 else "default"
        
        capture = ResponseCapture()
        print(f"Capturing: {url}")
        
        try:
            resp = capture.capture(url)
            meta_path, body_path = capture.save(resp, doc_name)
            print(f"Saved to:")
            print(f"  Meta: {meta_path}")
            print(f"  Body: {body_path}")
            print(f"  Slug: {capture.url_to_slug(url)}")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print(f"Unknown command: {sys.argv[1]}")
        sys.exit(1)
