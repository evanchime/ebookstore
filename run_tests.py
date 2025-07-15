#!/usr/bin/env python3
"""
Main test runner for the ebookstore project.
This script runs the complete test suite from the project root.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Change to tests directory and run the test suite
if __name__ == "__main__":
    import subprocess
    
    # Get the absolute path to the tests directory
    tests_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')
    
    # Run the test runner from the tests directory
    try:
        result = subprocess.run([
            sys.executable, 'run_all_tests.py'
        ], cwd=tests_dir, capture_output=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)
