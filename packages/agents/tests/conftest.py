"""Test configuration for mcpturbo_agents"""

import pytest
import sys
from pathlib import Path

# Add package to Python path
package_dir = Path(__file__).parent.parent
sys.path.insert(0, str(package_dir))


@pytest.fixture
def package_name():
    """Package name fixture"""
    return "mcpturbo_agents"


@pytest.fixture
def sample_data():
    """Sample data for tests"""
    return {
        "test_mode": True,
        "environment": "test"
    }
