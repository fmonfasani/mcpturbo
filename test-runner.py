#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test runner that handles empty packages gracefully"""

import subprocess
import sys
from pathlib import Path


def run_tests_for_package(package_path):
    """Run tests for a single package"""
    package_name = package_path.name
    tests_dir = package_path / "tests"

    if not tests_dir.exists():

        print(f"WARNING: No tests directory for {package_name}")
        return True

    test_files = list(tests_dir.glob("test_*.py"))
    if not test_files:
        print(f"WARNING: No test files in {package_name}")
        return True

    print(f"Running tests for {package_name}...")


    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/", "-v"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print(f"PASS: {package_name} tests passed")
            return True
        else:
            print(f"FAIL: {package_name} tests failed")

            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"ERROR: running tests for {package_name}: {e}")

        return False


def main():
    packages_dir = Path("packages")

    if not packages_dir.exists():

        print("ERROR: No packages directory found")
        sys.exit(1)

    packages = [d for d in packages_dir.iterdir() if d.is_dir()]
    print(f"Running tests for {len(packages)} packages...")


    passed = 0
    failed = 0

    for package in packages:
        if run_tests_for_package(package):
            passed += 1
        else:
            failed += 1


    print(f"\nTest Results: {passed} passed, {failed} failed")

    if failed > 0:
        print("Some tests failed")
        sys.exit(1)
    else:
        print("All tests passed!")

        sys.exit(0)


if __name__ == "__main__":
    main()
