"""HTTP Response capture system for real-world testing fixtures."""
import json
import re
import hashlib
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
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
    
    def save(self, captured: CapturedResponse, doc_name: str) -> tuple[Path, Path]:
        """Save captured response as .meta.json + .body.html pair."""
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
        
        # Write metadata
        meta = {
            "status": captured.status,
            "headers": captured.headers,
            "original_url": captured.url,
            "captured_at": captured.captured_at,
            "slug": slug
        }
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2)
        
        # Write body
        with open(body_path, 'w', encoding='utf-8') as f:
            f.write(captured.body)
        
        return meta_path, body_path
    
    def load(self, doc_name: str, slug: str) -> CapturedResponse:
        """Load captured response from disk."""
        doc_dir = self.fixtures_dir / doc_name
        
        with open(doc_dir / f"{slug}.meta.json", 'r', encoding='utf-8') as f:
            meta = json.load(f)
        
        with open(doc_dir / f"{slug}.body.html", 'r', encoding='utf-8') as f:
            body = f.read()
        
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
