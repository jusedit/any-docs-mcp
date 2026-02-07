"""Structured progress logging for scraper operations."""
import json
import sys
from datetime import datetime
from typing import TextIO, Optional


class ProgressLogger:
    """Structured JSONL progress logger for CI-friendly output."""
    
    def __init__(self, output: Optional[TextIO] = None):
        self.output = output or sys.stderr
    
    def _log(self, phase: str, current: int = 0, total: int = 0, 
             url: str = "", message: str = ""):
        """Write a structured JSON log line."""
        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "phase": phase,
            "current": current,
            "total": total,
            "url": url,
            "message": message
        }
        # JSONL format: one JSON object per line
        print(json.dumps(event), file=self.output)
        
        # Legacy PROGRESS: prefix for backward compatibility
        if phase in ['discovering', 'scraping', 'completed']:
            print(f"PROGRESS:{json.dumps(event)}", file=sys.stdout)
    
    def start(self, message: str = "Starting operation"):
        """Log operation start."""
        self._log("started", message=message)
    
    def update(self, current: int, total: int, url: str = "", message: str = ""):
        """Log progress update."""
        self._log("in_progress", current, total, url, message)
    
    def complete(self, current: int, total: int, message: str = ""):
        """Log operation completion."""
        self._log("completed", current, total, "", message)
    
    def fail(self, url: str, message: str):
        """Log operation failure."""
        self._log("failed", url=url, message=message)
