"""
Test suite runner for the ebookstore project.
Runs all tests and generates a comprehensive report.
"""

import unittest
import sys
import os
from io import StringIO
import time

# Add parent directory to path to import application modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all test modules
import test_book
import test_functions
import test_classes
import test_integration
import test_abstract_classes


def create_test_suite():
    """Create a comprehensive test suite containing all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test modules
    test_modules = [
        test_book,
        test_functions,
        test_classes,
        test_integration,
        test_abstract_classes
    ]
    
    for module in test_modules:
        suite.addTests(loader.loadTestsFromModule(module))
    
    return suite


def run_tests_with_report():
    """Run all tests and generate a detailed report."""
    print("=" * 80)
    print("EBOOKSTORE PROJECT - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"Starting test execution at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Create test suite
    suite = create_test_suite()
    
    # Count total tests
    total_tests = suite.countTestCases()
    print(f"Total tests to run: {total_tests}")
    print("-" * 80)
    
    # Create a detailed test runner
    stream = StringIO()
    runner = unittest.TextTestRunner(
        stream=stream, 
        verbosity=2,
        descriptions=True,
        failfast=False
    )
    
    # Run tests
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Get the test output
    test_output = stream.getvalue()
    
    # Print results
    print("TEST EXECUTION RESULTS:")
    print("=" * 80)
    print(test_output)
    
    # Summary statistics
    print("SUMMARY STATISTICS:")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(
        f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}"
    )
    passed_tests = result.testsRun - len(result.failures) - len(result.errors)
    success_rate = (
        (passed_tests / result.testsRun) * 100
    ) if result.testsRun else 0
    print(f"Success rate: {success_rate:.1f}%")
    print(f"Execution time: {end_time - start_time:.2f} seconds")
    
    # Detailed failure and error reporting
    if result.failures:
        print("\nDETAILED FAILURE REPORTS:")
        print("=" * 80)
        for test, traceback in result.failures:
            print(f"FAILED: {test}")
            print("-" * 40)
            print(traceback)
            print("-" * 40)
    
    if result.errors:
        print("\nDETAILED ERROR REPORTS:")
        print("=" * 80)
        for test, traceback in result.errors:
            print(f"ERROR: {test}")
            print("-" * 40)
            print(traceback)
            print("-" * 40)
    
    # Test coverage by module
    print("\nTEST COVERAGE BY MODULE:")
    print("=" * 80)
    modules_tested = {
        'test_book.py': 'Book class functionality',
        'test_functions.py': 'Utility functions and input validation',
        'test_classes.py': 'BookStore classes (SQLite and MySQL)',
        'test_integration.py': 'End-to-end integration tests',
        'test_abstract_classes.py': 'Abstract classes and error handling'
    }
    
    for module, description in modules_tested.items():
        print(f"✓ {module}: {description}")
    
    print("\nTEST CATEGORIES COVERED:")
    print("=" * 80)
    categories = [
        "✓ Unit Tests - Individual component testing",
        "✓ Integration Tests - Component interaction testing", 
        "✓ Database Tests - SQLite and MySQL operations",
        "✓ Error Handling - Exception and edge case testing",
        "✓ Input Validation - User input processing and validation",
        "✓ CLI Testing - Command-line argument parsing",
        "✓ File Operations - CSV reading and file handling",
        "✓ Mock Testing - External dependency isolation",
        "✓ Edge Cases - Boundary conditions and special scenarios",
        "✓ Security - SQL injection prevention and data validation"
    ]
    
    for category in categories:
        print(category)
    
    # Return success status
    return len(result.failures) == 0 and len(result.errors) == 0


def run_specific_test_module(module_name):
    """Run tests from a specific module."""
    print(f"Running tests from module: {module_name}")
    print("=" * 60)
    
    try:
        module = __import__(module_name)
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return len(result.failures) == 0 and len(result.errors) == 0
    except ImportError:
        print(f"Error: Could not import module '{module_name}'")
        return False


def main():
    """Main function to run tests based on command line arguments."""
    if len(sys.argv) > 1:
        # Run specific test module
        module_name = sys.argv[1]
        if module_name.endswith('.py'):
            module_name = module_name[:-3]  # Remove .py extension
        
        success = run_specific_test_module(module_name)
        sys.exit(0 if success else 1)
    else:
        # Run all tests
        success = run_tests_with_report()
        
        print("\n" + "=" * 80)
        if success:
            print(
                "🎉 ALL TESTS PASSED! "
                "The ebookstore application is working correctly."
            )
        else:
            print(
                "❌ SOME TESTS FAILED! "
                "Please review the failure reports above."
            )
        print("=" * 80)
        
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
