#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test runner que maneja packages vacíos gracefully"""


import subprocess
import sys
from pathlib import Path


def run_tests_for_package(package_path):
    """Run tests for a single package"""
    package_name = package_path.name
    tests_dir = package_path / "tests"

    if not tests_dir.exists():

        print(f"â ï¸ No tests directory for {package_name}")

        return True  # Success - no tests to run

    test_files = list(tests_dir.glob("test_*.py"))
    if not test_files:

        print(f"â ï¸ No test files in {package_name}")
        return True  # Success - no tests to run
    
    print(f"í·ª Running tests for {package_name}...")
    

    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/", "-v"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:

            print(f"â {package_name} tests passed")
            return True
        else:
            print(f"â {package_name} tests failed")

            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:

        print(f"â Error running tests for {package_name}: {e}")

        return False


def main():
    """Main test runner"""
    packages_dir = Path("packages")

    if not packages_dir.exists():

        print("â No packages directory found")

        sys.exit(1)

    packages = [d for d in packages_dir.iterdir() if d.is_dir()]

    
    print(f"í·ª Running tests for {len(packages)} packages...")
    

    passed = 0
    failed = 0

    for package in packages:
        if run_tests_for_package(package):
            passed += 1
        else:
            failed += 1

    
    print(f"\ní³ Test Results: {passed} passed, {failed} failed")
    
    if failed > 0:
        print("â Some tests failed")
        sys.exit(1)
    else:
        print("â All tests passed!")

        sys.exit(0)


if __name__ == "__main__":
    main()
