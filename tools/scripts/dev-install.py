#!/usr/bin/env python3
"""Install all packages in development mode"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run shell command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {cmd}: {e}")
        return False

def main():
    """Install all packages in dev mode"""
    root_dir = Path(__file__).parent.parent.parent
    packages_dir = root_dir / "packages"
    
    packages = [d for d in packages_dir.iterdir() if d.is_dir()]
    
    print(f"� Installing {len(packages)} packages in development mode...")
    
    for package in packages:
        pyproject = package / "pyproject.toml"
        if pyproject.exists():
            print(f"� Installing {package.name} in dev mode...")
            success = run_command("pip install -e .", cwd=package)
            if success:
                print(f"✅ {package.name} installed")
            else:
                print(f"❌ {package.name} installation failed")
                return False
    
    print(f"\n� All packages installed in development mode!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
