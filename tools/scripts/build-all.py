#!/usr/bin/env python3
"""Build script for all MCPTurbo packages"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run shell command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running {cmd}: {result.stderr}")
            return False
        print(result.stdout)
        return True
    except Exception as e:
        print(f"Exception running {cmd}: {e}")
        return False

def main():
    """Main build function"""
    root_dir = Path(__file__).parent.parent.parent
    packages_dir = root_dir / "packages"
    
    packages = [d for d in packages_dir.iterdir() if d.is_dir()]
    
    print(f"Ì¥® Building {len(packages)} packages...")
    
    success_count = 0
    for package in packages:
        print(f"\nÌ≥¶ Building {package.name}...")
        
        # Check if pyproject.toml exists
        pyproject = package / "pyproject.toml"
        if pyproject.exists():
            # Use modern Python build
            success = run_command("python -m build", cwd=package)
            if success:
                print(f"‚úÖ {package.name} built successfully")
                success_count += 1
            else:
                print(f"‚ùå {package.name} build failed")
        else:
            print(f"‚ö†Ô∏è No pyproject.toml found in {package.name}, skipping...")
    
    print(f"\nÌæâ Build completed: {success_count}/{len(packages)} packages built successfully!")
    return success_count == len([p for p in packages if (p / "pyproject.toml").exists()])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
