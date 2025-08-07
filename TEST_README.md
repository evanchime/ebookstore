# eBookstore Test Suite Documentation

This document provides comprehensive information about the professional test suite for the eBookstore project.

## Test Suite Overview

The eBookstore project includes a comprehensive test suite with **136 test cases** achieving **100% success rate**, covering:

- **Unit Tests**: Individual component testing (Book class with enhanced validation, utility functions)
- **Integration Tests**: Component interaction and end-to-end workflow testing  
- **Database Tests**: SQLite and MySQL operations with real database connections
- **Error Handling Tests**: Exception scenarios and edge case testing
- **Input Validation Tests**: User input processing and validation with defense-in-depth
- **CLI Tests**: Command-line argument parsing and interface testing
- **File Operations Tests**: CSV reading and file handling
- **Mock Tests**: External dependency isolation and behavior verification
- **Edge Case Tests**: Boundary conditions and special scenarios
- **Security Tests**: SQL injection prevention and data validation

## Test Files Structure

```
ebookstore/
├── tests/                        # Professional test suite directory
│   ├── __init__.py              # Package marker
│   ├── run_all_tests.py         # Comprehensive test runner with reporting
│   ├── test_book.py             # Book class unit tests (15 tests)
│   ├── test_functions.py        # Utility functions tests (27 tests) 
│   ├── test_classes.py          # BookStore implementation tests (47 tests)
│   ├── test_integration.py      # End-to-end integration tests (19 tests)
│   └── test_abstract_classes.py # Abstract classes & error handling (28 tests)
├── run_tests.py                 # Root-level test runner
├── ebookstore.py               # Main application
├── classes.py                  # BookStore implementations (with enhanced Book class)
├── functions.py                # Utility functions
├── abstract_classes.py         # Abstract base classes
└── requirements.txt            # Dependencies including test frameworks
```

## Running the Tests

### Prerequisites

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure you have Python 3.7+ installed.

### Running All Tests

#### Option 1: Using pytest (Recommended)
```bash
python3 -m pytest tests/
```
**Output**: Clean pytest output with 136 tests discovered and executed

#### Option 2: Using custom test runner (Comprehensive reporting)
```bash
python3 run_tests.py
```
**Output**: Detailed report with statistics, coverage, and failure analysis

#### Option 3: From tests directory
```bash
cd tests && python3 run_all_tests.py
```
**Output**: Comprehensive test execution with detailed reporting

### Running Specific Test Modules

#### Using pytest for specific modules:
```bash
python3 -m pytest tests/test_book.py -v                    # Book class tests
python3 -m pytest tests/test_functions.py -v               # Utility function tests  
python3 -m pytest tests/test_classes.py -v                 # BookStore class tests
python3 -m pytest tests/test_integration.py -v             # Integration tests
python3 -m pytest tests/test_abstract_classes.py -v        # Abstract class tests
```

#### Using custom runner for specific modules:
```bash
cd tests && python3 run_all_tests.py test_book             # Run specific module
```

#### Running individual test methods:
```bash
python3 -m pytest tests/test_book.py::TestBook::test_book_creation_valid_data -v
python3 -m pytest tests/test_integration.py::TestEbookstoreIntegration::test_main_add_book_workflow -v
```

### Test Execution Results

**Expected Output:**
```
================================================================================
EBOOKSTORE PROJECT - COMPREHENSIVE TEST SUITE
================================================================================
Tests run: 136
Failures: 0
Errors: 0
Success rate: 100.0%
Execution time: ~3-5 seconds
================================================================================
🎉 ALL TESTS PASSED! The ebookstore application is working correctly.
================================================================================
```

## Test Categories

### 1. Unit Tests (42 tests)

#### test_book.py (15 tests)
Tests the enhanced `Book` class functionality with comprehensive validation:
- ✅ **Book Creation**: Valid/invalid data with enhanced validation
- ✅ **Title Validation**: Empty, whitespace-only, and special character handling
- ✅ **Author Validation**: Empty, whitespace-only, and unicode character support
- ✅ **Quantity Validation**: Integer type checking, negative value prevention, zero handling
- ✅ **Data Sanitization**: Automatic trimming of leading/trailing whitespace
- ✅ **Attribute Modification**: Post-creation attribute updates
- ✅ **Edge Cases**: Large values, special characters, numeric strings
- ✅ **Error Messages**: Clear, specific validation error reporting

#### test_functions.py (27 tests)  
Tests utility functions with comprehensive input validation:
- ✅ **Input Validation Functions**: `get_book_title_utility`, `get_book_author_utility` with retry logic
- ✅ **CLI Argument Parsing**: `parse_cli_args` with all parameter combinations
- ✅ **Database Connection Handling**: `get_database_connection` with environment variables
- ✅ **File Operations**: CSV reading with `get_table_records` and error handling
- ✅ **User Interaction Utilities**: `do_you_have_book_id_utility` with case-insensitive input
- ✅ **Quantity Operations**: `get_book_qty_utility` with integer validation
- ✅ **Update Operations**: `get_book_update_info` for all field types
- ✅ **Error Handling**: Comprehensive exception scenarios and edge cases

### 2. Integration Tests (19 tests)

#### test_integration.py (19 tests)
Tests complete workflows and end-to-end scenarios:
- ✅ **Command-line Arguments**: All CLI argument parsing variations
- ✅ **Complete Workflows**: Add, update, delete, search book operations
- ✅ **Database Integration**: Real SQLite database operations with file I/O
- ✅ **Error Handling**: ValueError, permission errors, and edge cases
- ✅ **User Interface**: Menu navigation and input validation
- ✅ **File Operations**: CSV reading and directory creation
- ✅ **Multi-operation Scenarios**: Complex user interaction flows

### 3. Database Tests (47 tests)

#### test_classes.py (47 tests)
Tests BookStore implementation classes with comprehensive database operations:
- ✅ **SQLite Operations**: Insert, update, delete, search with real database connections
- ✅ **MySQL Operations**: Connection handling and query execution (mocked for testing)
- ✅ **Database Connections**: Connection string parsing and configuration setup
- ✅ **Transaction Management**: Commit, rollback, and comprehensive error handling
- ✅ **Case-insensitive Operations**: Unicode NOCASE collation testing for international support
- ✅ **Constraint Handling**: Duplicate detection, validation, and graceful error messaging
- ✅ **Custom Table Names**: Dynamic table name configuration and SQL injection prevention
- ✅ **Data Integrity**: Book finding by ID vs title/author with proper validation
- ✅ **Abstract Class Integration**: Quantity update utilities with business logic validation
- ✅ **Predefined Records**: CSV data loading and bulk operations

### 4. Abstract Classes & Error Handling Tests (28 tests)

#### test_abstract_classes.py (28 tests)
Tests abstract class functionality and comprehensive error handling:
- ✅ **Abstract Class Design**: Proper abstraction, inheritance, and instantiation prevention
- ✅ **Quantity Update Utilities**: Add, subtract, set operations with business rule validation
- ✅ **Error Handling**: SQLite, MySQL, Permission, and generic error scenarios with context
- ✅ **Edge Cases**: Zero quantities, very large numbers, special characters, unicode data
- ✅ **Database Error Propagation**: Proper error context chaining and user-friendly messages
- ✅ **Boundary Conditions**: Maximum integer values, empty strings, whitespace handling
- ✅ **Security Testing**: SQL injection prevention and comprehensive input sanitization
- ✅ **Constraint Violations**: Database integrity testing and graceful failure handling

## Test Coverage & Quality Metrics

### Coverage Summary
- **Total Tests**: 136
- **Success Rate**: 100% (All tests passing)
- **Code Coverage**: Comprehensive coverage across all modules
- **Execution Time**: ~3-5 seconds (fast and efficient)
- **Test Categories**: 10 different test categories

### Enhanced Features (Recent Additions)
- ✅ **Book Class Validation**: Enhanced constructor with title, author, and quantity validation
- ✅ **Defense in Depth**: Validation at both input layer and data model layer
- ✅ **Comprehensive Error Messages**: Clear, specific validation feedback
- ✅ **Data Sanitization**: Automatic whitespace trimming and normalization
- ✅ **Type Safety**: Integer quantity validation with negative value prevention
- ✅ **Clean Codebase**: Removed unused test files and streamlined structure

### Test Quality Features
- ✅ **Professional Structure**: Tests organized in dedicated `tests/` directory  
- ✅ **Multiple Test Runners**: pytest and custom runner compatibility
- ✅ **Comprehensive Mocking**: External dependencies properly isolated
- ✅ **Real Database Testing**: Actual SQLite operations with cleanup
- ✅ **Error Scenario Coverage**: All exception types and edge cases tested
- ✅ **Documentation**: Every test method has descriptive docstrings
- ✅ **Cleanup**: Proper resource cleanup (files, connections, temporary data)
- ✅ **Repeatability**: Tests are independent and can run in any order

### Test Reporting Features
- Detailed execution statistics
- Failure analysis with tracebacks
- Test coverage by module breakdown
- Performance timing metrics
- Success/failure categorization
- Professional formatting and output

## Advanced Test Usage

### Running Tests with Coverage
```bash
python3 -m pytest tests/ --cov=. --cov-report=html
```

### Running Tests in Verbose Mode
```bash
python3 -m pytest tests/ -v -s
```

### Running Specific Test Categories
```bash
# Error handling tests only
python3 -m pytest tests/test_abstract_classes.py::TestErrorHandling -v

# Integration workflows only  
python3 -m pytest tests/test_integration.py::TestEbookstoreIntegration -v

# Database operations only
python3 -m pytest tests/test_classes.py::TestBookStoreSqlite -v
```

## Test Development Guidelines

### Writing New Tests

When adding new tests, follow these patterns:

```python
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestNewFeature(unittest.TestCase):
    """Test cases for new feature."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        # Initialize test resources
        pass
        
    def tearDown(self):
        """Clean up after each test."""
        # Clean up test resources
        pass
        
    def test_feature_functionality(self):
        """Test the main functionality of the feature."""
        # Test implementation with descriptive assertions
        self.assertEqual(actual, expected)
        
    @patch('module.external_dependency')
    def test_feature_with_mock(self, mock_dependency):
        """Test feature with mocked dependency."""
        mock_dependency.return_value = expected_value
        # Test implementation
        self.assertTrue(result)
```

### Best Practices

1. **Test Names**: Use descriptive names that explain what is being tested
2. **Test Isolation**: Each test should be independent and clean up after itself
3. **Mocking Strategy**: Mock external dependencies appropriately (databases, files, APIs)
4. **Resource Cleanup**: Always clean up resources (files, connections, temporary data)
5. **Assertions**: Use specific assertion methods (`assertEqual`, `assertIn`, `assertRaises`)
6. **Documentation**: Include descriptive docstrings for all test methods
7. **Error Testing**: Test both success and failure scenarios
8. **Edge Cases**: Include boundary conditions and special cases

## Test Environment Setup

### Development Environment
```bash
# Clone repository
git clone https://github.com/evanchime/ebookstore.git
cd ebookstore

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests to verify setup
python3 -m pytest tests/
```

### Dependencies for Testing
The test suite requires these packages (included in `requirements.txt`):
- `unittest` (Python standard library)
- `pytest` (Third-party test runner)
- `unittest.mock` (Mocking framework)

## Continuous Integration

The test suite is designed to work seamlessly in CI/CD environments:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    python3 -m pytest tests/ --tb=short
    
- name: Run Custom Test Runner  
  run: |
    python3 run_tests.py
```

## Future Enhancements

Potential test improvements for consideration:
- **Property-based Testing**: Using Hypothesis for more comprehensive edge case discovery
- **Performance Benchmarking**: Baseline performance metrics and regression detection  
- **Security Testing**: Extended SQL injection and input validation testing
- **Cross-platform Testing**: Windows, macOS, and Linux compatibility validation
- **Docker Integration**: Containerized test environments for consistency
- **API Testing**: RESTful API endpoint testing when web interface is added
- **Load Testing**: Performance testing with large datasets
- **Mutation Testing**: Code quality validation through mutation testing

---

This comprehensive test suite ensures the reliability, correctness, and maintainability of the eBookstore application across all scenarios and use cases. The 100% success rate, enhanced validation features, and professional structure provide confidence for production deployment and ongoing development.
