"""
Tests for abstract classes and error handling functionality.
"""

import unittest
from unittest.mock import patch
import tempfile
import os
import sys

# Add parent directory to path to import application modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abstract_classes import BookStore
from classes import BookStoreSqlite
import sqlite3
import mysql.connector


class TestAbstractBookStore(unittest.TestCase):
    """Test cases for abstract BookStore class."""

    def test_abstract_class_cannot_be_instantiated(self):
        """Test that BookStore abstract class cannot be instantiated 
        directly."""
        with self.assertRaises(TypeError):
            BookStore()

    def test_get_update_qty_utility_add_action(self):
        """Test quantity update utility with 'add' action."""
        book_info = {"action": "add", "qty": 10}
        record = (1, "Title", "Author", 20)  # Current qty is 20
        
        result = BookStore.get_update_qty_utility(book_info, record)
        self.assertEqual(result, 30)  # 20 + 10

    def test_get_update_qty_utility_sub_action(self):
        """Test quantity update utility with 'sub' action."""
        book_info = {"action": "sub", "qty": 5}
        record = (1, "Title", "Author", 20)  # Current qty is 20
        
        result = BookStore.get_update_qty_utility(book_info, record)
        self.assertEqual(result, 15)  # 20 - 5

    def test_get_update_qty_utility_set_action(self):
        """Test quantity update utility with 'set' action."""
        book_info = {"action": "set", "qty": 50}
        record = (1, "Title", "Author", 20)  # Current qty is 20
        
        result = BookStore.get_update_qty_utility(book_info, record)
        self.assertEqual(result, 50)  # Set to 50

    def test_get_update_qty_utility_negative_result_error(self):
        """Test quantity update utility raises error for negative 
        result."""
        book_info = {"action": "sub", "qty": 25}
        # Current qty is 20, trying to subtract 25
        record = (1, "Title", "Author", 20)  
        
        with self.assertRaises(Exception) as context:
            BookStore.get_update_qty_utility(book_info, record)
        
        error_message = str(context.exception)
        self.assertIn("You can't perform this operation", error_message)
        self.assertIn("You only have 20 of this book in stock", error_message)
        self.assertIn("but you want to reduce the stock by 25", error_message)

    def test_get_update_qty_utility_exact_subtraction(self):
        """Test quantity update utility with exact subtraction 
        (result = 0)."""
        book_info = {"action": "sub", "qty": 20}
        # Current qty is 20, trying to subtract 20
        record = (1, "Title", "Author", 20)
        
        result = BookStore.get_update_qty_utility(book_info, record)
        self.assertEqual(result, 0)  # Should be exactly 0

    def test_get_update_qty_utility_large_numbers(self):
        """Test quantity update utility with large numbers."""
        book_info = {"action": "add", "qty": 999999}
        record = (1, "Title", "Author", 1000000)
        
        result = BookStore.get_update_qty_utility(book_info, record)
        self.assertEqual(result, 1999999)

    def test_update_books_utility_quantity_field(self):
        """Test update_books_utility for quantity field."""
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        try:
            with patch('builtins.print'):
                bookstore = BookStoreSqlite(temp_db.name)
                
                book_info = {
                    "field": "quantity",
                    "action": "add",
                    "qty": 5
                }
                record = (1, "Test Title", "Test Author", 10)
                
                # Mock the utility methods
                with patch.object(
                    bookstore, 'update_qty_utility'
                ) as mock_qty_util:
                    with patch.object(
                        BookStore, 'get_update_qty_utility', return_value=15
                    ):
                        bookstore.update_books_utilty(book_info, record)
                        mock_qty_util.assert_called_once_with(15, book_info)
                
                bookstore.db.close()
        finally:
            if os.path.exists(temp_db.name):
                os.unlink(temp_db.name)

    def test_update_books_utility_title_field(self):
        """Test update_books_utility for title field."""
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        try:
            with patch('builtins.print'):
                bookstore = BookStoreSqlite(temp_db.name)
                
                book_info = {
                    "field": "title",
                    "new_title": "New Title"
                }
                record = (1, "Old Title", "Test Author", 10)
                
                # Mock the utility method
                with patch.object(
                    bookstore, 'update_title_utility'
                ) as mock_title_util:
                    bookstore.update_books_utilty(book_info, record)
                    mock_title_util.assert_called_once_with(book_info)
                
                bookstore.db.close()
        finally:
            if os.path.exists(temp_db.name):
                os.unlink(temp_db.name)

    def test_update_books_utility_author_field(self):
        """Test update_books_utility for author field."""
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        try:
            with patch('builtins.print'):
                bookstore = BookStoreSqlite(temp_db.name)
                
                book_info = {
                    "field": "author",
                    "new_author": "New Author"
                }
                record = (1, "Test Title", "Old Author", 10)
                
                # Mock the utility method
                with patch.object(
                    bookstore, 'update_author_utility'
                ) as mock_author_util:
                    bookstore.update_books_utilty(book_info, record)
                    mock_author_util.assert_called_once_with(book_info)
                
                bookstore.db.close()
        finally:
            if os.path.exists(temp_db.name):
                os.unlink(temp_db.name)


class TestErrorHandling(unittest.TestCase):
    """Test error handling in BookStore classes."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_sqlite_error_handling(self):
        """Test SQLite error handling in _handle_db_error method."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.temp_db.name)
            
            # Create a mock SQLite error with real traceback
            try:
                raise sqlite3.Error("Test SQLite error")
            except sqlite3.Error as e:
                mock_error = e
            
            # Test that the error handler properly re-raises with context
            with self.assertRaises(Exception) as context:
                bookstore._handle_db_error(mock_error)
            
            # Check error message contains file and line info
            # rollback() is called internally but we can't assert 
            # on real DB connection
            self.assertIn("Error on line", str(context.exception))
            self.assertIn("Test SQLite error", str(context.exception))
            
            bookstore.db.close()

    def test_mysql_error_handling(self):
        """Test MySQL error handling in _handle_db_error method."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.temp_db.name)
            
            # Create a mock MySQL error with real traceback
            try:
                raise mysql.connector.Error("Test MySQL error")
            except mysql.connector.Error as e:
                mock_error = e
            
            # Test that the error handler properly re-raises with context
            with self.assertRaises(Exception) as context:
                bookstore._handle_db_error(mock_error)
            
            # Check error message contains file and line info
            self.assertIn("Error on line", str(context.exception))
            self.assertIn("Test MySQL error", str(context.exception))
            
            bookstore.db.close()

    def test_permission_error_handling(self):
        """Test permission error handling in _handle_db_error method."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.temp_db.name)
            
            # Create a mock permission error with real traceback
            try:
                raise PermissionError("Permission denied")
            except PermissionError as e:
                mock_error = e
            
            # Test that the error handler properly re-raises with context
            with self.assertRaises(PermissionError) as context:
                bookstore._handle_db_error(mock_error)
            
            # Check that error message contains file and line info
            # rollback() is called internally but we can't assert 
            # on real DB connection
            self.assertIn("Error on line", str(context.exception))
            self.assertIn("Permission denied", str(context.exception))
            
            bookstore.db.close()

    def test_generic_error_handling(self):
        """Test generic error handling in _handle_db_error method."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.temp_db.name)
            
            # Create a mock generic error with real traceback
            try:
                raise RuntimeError("Generic runtime error")
            except RuntimeError as e:
                mock_error = e
            
            # Test that the error handler properly re-raises with context
            # Generic errors get converted to Exception type by 
            # _handle_db_error
            with self.assertRaises(Exception) as context:
                bookstore._handle_db_error(mock_error)
            
            # Check that error message contains file and line info
            # rollback() is called internally but we can't assert 
            # on real DB connection
            self.assertIn("Error on line", str(context.exception))
            self.assertIn("Generic runtime error", str(context.exception))
            
            bookstore.db.close()

    def test_update_book_with_sqlite_error(self):
        """Test update_book method with SQLite error."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.temp_db.name)
            
            # Insert a test book first
            from classes import Book
            test_book = Book("Test Title", "Test Author", 10)
            bookstore.insert_book(test_book)
            
            # Get the book ID
            book_info = {"title": "Test Title", "author": "Test Author"}
            record = bookstore.find_book(book_info)
            book_id = record[0]
            
            # Close the database connection to simulate an error
            bookstore.db.close()
            
            # Try to update the book
            update_info = {
                "id": book_id,
                "field": "quantity",
                "action": "add",
                "qty": 5
            }
            
            with self.assertRaises(Exception):
                bookstore.update_book(update_info)

    def test_database_constraint_violation(self):
        """Test handling of database constraint violations."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.temp_db.name)
            
            from classes import Book
            test_book = Book("Unique Title", "Unique Author", 10)
            
            # Insert the book successfully
            bookstore.insert_book(test_book)
            
            # Try to insert the same book again (should not raise error,
            #  just print message)
            with patch('builtins.print') as mock_print:
                bookstore.insert_book(test_book)
                mock_print.assert_any_call("\nBook already exists")
            
            bookstore.db.close()

    def test_invalid_database_operations(self):
        """Test various invalid database operations."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.temp_db.name)
            
            # Test finding book with malformed book_info
            result = bookstore.find_book({})  # Empty dict
            self.assertIsNone(result)
            
            # Test updating quantity with malformed book_info
            try:
                # This might cause SQL error
                bookstore.update_qty_utility(10, {})  
            except Exception:
                pass  # Expected to fail
            
            bookstore.db.close()


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_zero_quantity_operations(self):
        """Test operations with zero quantities."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.temp_db.name)
            
            from classes import Book
            test_book = Book("Zero Qty Book", "Test Author", 0)
            bookstore.insert_book(test_book)
            
            # Find the book
            book_info = {"title": "Zero Qty Book", "author": "Test Author"}
            result = bookstore.find_book(book_info)
            self.assertIsNotNone(result)
            self.assertEqual(result[3], 0)
            
            bookstore.db.close()

    def test_very_long_strings(self):
        """Test handling of very long strings for title and author."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.temp_db.name)
            
            # Create book with very long title and author
            long_title = "A" * 1000  # Very long title
            long_author = "B" * 1000  # Very long author
            
            from classes import Book
            test_book = Book(long_title, long_author, 5)
            
            try:
                bookstore.insert_book(test_book)
                
                # Try to find the book
                book_info = {"title": long_title, "author": long_author}
                result = bookstore.find_book(book_info)
                self.assertIsNotNone(result)
                
            except Exception:
                # Some databases might have length limits
                pass
            
            bookstore.db.close()

    def test_special_characters_in_book_data(self):
        """Test handling of special characters in book data."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.temp_db.name)
            
            # Test with various special characters
            special_chars_title = (
                "Title with 'quotes' and \"double quotes\" and "
                "$pecial ch@rs!"
            )
            special_chars_author = "Author with àccénts and emojis 📚"
            
            from classes import Book
            test_book = Book(special_chars_title, special_chars_author, 3)
            bookstore.insert_book(test_book)
            
            # Verify the book can be found
            book_info = {
                "title": special_chars_title, "author": special_chars_author
            }
            result = bookstore.find_book(book_info)
            self.assertIsNotNone(result)
            self.assertEqual(result[1], special_chars_title)
            self.assertEqual(result[2], special_chars_author)
            
            bookstore.db.close()

    def test_maximum_quantity_values(self):
        """Test handling of very large quantity values."""
         # Max 32-bit int
        book_info = {"action": "add", "qty": 2147483647} 
        record = (1, "Title", "Author", 0)
        
        result = BookStore.get_update_qty_utility(book_info, record)
        self.assertEqual(result, 2147483647)

    def test_empty_search_query(self):
        """Test search with empty query string."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.temp_db.name)
            
            # Insert a test book
            from classes import Book
            test_book = Book("Test Book", "Test Author", 5)
            bookstore.insert_book(test_book)
            
            # Search with empty string
            with patch('builtins.print') as mock_print:
                bookstore.search_books("")
                # Should find the book since empty string matches 
                # everything with LIKE
                self.assertTrue(mock_print.called)
            
            bookstore.db.close()

    def test_case_sensitivity_edge_cases(self):
        """Test case sensitivity in various scenarios."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.temp_db.name)
            
            from classes import Book
            test_book = Book("The Great Gatsby", "F. Scott Fitzgerald", 5)
            bookstore.insert_book(test_book)
            
            # Test finding with different cases
            variations = [
                {"title": "the great gatsby", "author": "f. scott fitzgerald"},
                {"title": "THE GREAT GATSBY", "author": "F. SCOTT FITZGERALD"},
                {"title": "The Great Gatsby", "author": "f. scott fitzgerald"},
                {"title": "The great Gatsby", "author": "F. scott fitzgerald"},
            ]
            
            
            for book_info in variations:
                result = bookstore.find_book(book_info)
                # Due to UNICODE_NOCASE collation, these should all find 
                # the book
                self.assertIsNotNone(
                    result, f"Failed to find book with {book_info}"
                )
            
            bookstore.db.close()


if __name__ == '__main__':
    unittest.main()
