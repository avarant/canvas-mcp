"""
Pytest configuration file.
"""

import os
import sys
import pytest

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Common fixtures can be added here
@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Set up test environment variables."""
    monkeypatch.setenv("CANVAS_TOKEN", "test_token")
    monkeypatch.setenv("CANVAS_HOST", "https://test.instructure.com") 