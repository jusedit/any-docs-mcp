"""Test progress logger functionality."""
import pytest
import json
from io import StringIO
from progress_logger import ProgressLogger


def test_progress_logger_logs_json():
    """ProgressLogger outputs valid JSON lines."""
    output = StringIO()
    logger = ProgressLogger(output)
    
    logger.start("Test operation")
    
    output.seek(0)
    line = output.readline()
    event = json.loads(line)
    
    assert event["phase"] == "started"
    assert "timestamp" in event
    assert event["message"] == "Test operation"


def test_progress_logger_update():
    """ProgressLogger update method logs progress."""
    output = StringIO()
    logger = ProgressLogger(output)
    
    logger.update(5, 10, "http://example.com", "Processing")
    
    output.seek(0)
    line = output.readline()
    event = json.loads(line)
    
    assert event["phase"] == "in_progress"
    assert event["current"] == 5
    assert event["total"] == 10
    assert event["url"] == "http://example.com"


def test_progress_logger_complete():
    """ProgressLogger complete method logs completion."""
    output = StringIO()
    logger = ProgressLogger(output)
    
    logger.complete(10, 10, "Done")
    
    output.seek(0)
    line = output.readline()
    event = json.loads(line)
    
    assert event["phase"] == "completed"
    assert event["current"] == 10
    assert event["total"] == 10


def test_progress_logger_fail():
    """ProgressLogger fail method logs errors."""
    output = StringIO()
    logger = ProgressLogger(output)
    
    logger.fail("http://example.com", "Connection error")
    
    output.seek(0)
    line = output.readline()
    event = json.loads(line)
    
    assert event["phase"] == "failed"
    assert event["url"] == "http://example.com"
    assert "error" in event["message"].lower() or "Connection" in event["message"]
