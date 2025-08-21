import sys
from pathlib import Path

# Add package src directory to Python path for tests
package_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(package_dir))
