# src/tests/conftest.py
import os
import sys
import pytest
from pathlib import Path

# Add src directory to Python path for imports
src_path = str(Path(__file__).parent.parent)
sys.path.insert(0, src_path)

# Set test environment variables
os.environ['ENVIRONMENT'] = 'test'
os.environ['ANTHROPIC_API_KEY'] = 'test_key'

@pytest.fixture(scope="function")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
