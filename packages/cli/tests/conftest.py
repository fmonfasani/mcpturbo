"""Test configuration for mcpturbo_cli"""

import pytest
import sys
from pathlib import Path

# Add package to Python path
package_dir = Path(__file__).parent.parent
sys.path.insert(0, str(package_dir))

# Ensure other project packages are importable
root_dir = package_dir.parent.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "packages" / "ai"))
sys.path.insert(0, str(root_dir / "packages" / "orchestrator"))


@pytest.fixture
def package_name():
    """Package name fixture"""
    return "mcpturbo_cli"


@pytest.fixture
def sample_data():
    """Sample data for tests"""
    return {
        "test_mode": True,
        "environment": "test"
    }
