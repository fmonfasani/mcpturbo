"""Test configuration for mcpturbo_core"""

import pytest
import sys
from pathlib import Path
import structlog

# Add package to Python path
package_dir = Path(__file__).parent.parent
sys.path.insert(0, str(package_dir / "src"))
# Ensure other packages in repository are importable
repo_root = package_dir.parent.parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(repo_root / "packages" / "agents" / "src"))

from mcpturbo_core.logger import configure_logging

configure_logging()


@pytest.fixture
def package_name():
    """Package name fixture"""
    return "mcpturbo_core"


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
