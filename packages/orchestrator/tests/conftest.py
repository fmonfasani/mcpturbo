"""Test configuration for mcpturbo_orchestrator"""

import pytest
import sys
from pathlib import Path
import structlog

# Add src packages to Python path
tests_dir = Path(__file__).parent
package_root = tests_dir.parent
root_dir = package_root.parent

sys.path.insert(0, str(package_root / "src"))
sys.path.insert(0, str(root_dir / "core" / "src"))
sys.path.insert(0, str(root_dir / "agents" / "src"))

from mcpturbo_core.logger import configure_logging

configure_logging()


@pytest.fixture
def package_name():
    """Package name fixture"""
    return "mcpturbo_orchestrator"


@pytest.fixture
def sample_data():
    """Sample data for tests"""
    return {
        "test_mode": True,
        "environment": "test"
    }


@pytest.fixture
def log_capture():
    """Capture structlog logs for assertions."""
    with structlog.testing.capture_logs() as captured:
        yield captured
