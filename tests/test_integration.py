"""
Integration tests for the main ebookstore application.
Tests the complete workflow and command-line interface.
"""

import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
import sys
from io import StringIO

# Add parent directory to path to import application modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ebookstore
from classes import BookStoreSqlite


class TestEbookstoreIntegration(unittest.TestCase):
    """Integration test cases for the main ebookstore application."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    @patch('sys.argv', ['ebookstore.py', '--database-file', 'test.db'])
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_add_book_workflow(self, mock_print, mock_input):
        """Test complete workflow for adding a book."""
        # Mock user inputs for adding a book
        mock_input.side_effect = [
            '1',  # Select "Enter book"
            'Test Book Title',  # Book title
            'Test Author',  # Book author
            '15',  # Book quantity
            '',  # Return to menu
            '0'   # Exit
        ]
        
        with patch('ebookstore.BookStoreSqlite') as mock_bookstore_class:
            mock_bookstore = MagicMock()
            mock_bookstore_class.return_value = mock_bookstore
            
            try:
                ebookstore.main()
            except SystemExit:
                pass  # Expected when exiting
            
            # Verify that insert_book was called
            mock_bookstore.insert_book.assert_called_once()
            
            # Verify the book object passed to insert_book
            book_arg = mock_bookstore.insert_book.call_args[0][0]
            self.assertEqual(book_arg.title, 'Test book title')
            self.assertEqual(book_arg.author, 'TEST AUTHOR')
            self.assertEqual(book_arg.qty, 15)

    @patch('sys.argv', ['ebookstore.py', '--database-file', 'test.db'])
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_update_book_workflow(self, mock_print, mock_input):
        """Test complete workflow for updating a book."""
        # Mock user inputs for updating a book
        mock_input.side_effect = [
            '2',  # Select "Update book"
            'yes',  # Have book ID
            '123',  # Book ID
            'quantity',  # Field to update
            'add',  # Action (add to quantity)
            '5',  # Quantity to add
            '',  # Return to menu
            '0'   # Exit
        ]
        
        with patch('ebookstore.BookStoreSqlite') as mock_bookstore_class:
            mock_bookstore = MagicMock()
            mock_bookstore_class.return_value = mock_bookstore
            
            try:
                ebookstore.main()
            except SystemExit:
                pass  # Expected when exiting
            
            # Verify that update_book was called
            mock_bookstore.update_book.assert_called_once()
            
            # Verify the book_info passed to update_book
            book_info = mock_bookstore.update_book.call_args[0][0]
            self.assertEqual(book_info['id'], 123)
            self.assertEqual(book_info['field'], 'quantity')
            self.assertEqual(book_info['action'], 'add')
            self.assertEqual(book_info['qty'], 5)

    @patch('sys.argv', ['ebookstore.py', '--database-file', 'test.db'])
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_delete_book_workflow(self, mock_print, mock_input):
        """Test complete workflow for deleting a book."""
        # Mock user inputs for deleting a book
        mock_input.side_effect = [
            '3',  # Select "Delete book"
            'no',  # Don't have book ID
            'Test Book',  # Book title
            'Test Author',  # Book author
            '',  # Return to menu
            '0'   # Exit
        ]
        
        with patch('ebookstore.BookStoreSqlite') as mock_bookstore_class:
            mock_bookstore = MagicMock()
            mock_bookstore_class.return_value = mock_bookstore
            
            try:
                ebookstore.main()
            except SystemExit:
                pass  # Expected when exiting
            
            # Verify that delete_book was called
            mock_bookstore.delete_book.assert_called_once()
            
            # Verify the book_info passed to delete_book
            book_info = mock_bookstore.delete_book.call_args[0][0]
            self.assertEqual(book_info['title'], 'Test book')
            self.assertEqual(book_info['author'], 'TEST AUTHOR')

    @patch('sys.argv', ['ebookstore.py', '--database-file', 'test.db'])
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_search_books_workflow(self, mock_print, mock_input):
        """Test complete workflow for searching books."""
        # Mock user inputs for searching books
        mock_input.side_effect = [
            '4',  # Select "Search books"
            'test search query',  # Search query
            '',  # Return to menu
            '0'   # Exit
        ]
        
        with patch('ebookstore.BookStoreSqlite') as mock_bookstore_class:
            mock_bookstore = MagicMock()
            mock_bookstore_class.return_value = mock_bookstore
            
            try:
                ebookstore.main()
            except SystemExit:
                pass  # Expected when exiting
            
            # Verify that search_books was called
            mock_bookstore.search_books.assert_called_once_with(
                'test search query'
            )

    @patch('sys.argv', ['ebookstore.py', '--database-file', 'test.db'])
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_invalid_menu_option(self, mock_print, mock_input):
        """Test handling of invalid menu options."""
        # Mock user inputs with invalid option
        mock_input.side_effect = [
            '99',  # Invalid option
            '0'    # Exit
        ]
        
        with patch('ebookstore.BookStoreSqlite') as mock_bookstore_class:
            mock_bookstore = MagicMock()
            mock_bookstore_class.return_value = mock_bookstore
            
            try:
                ebookstore.main()
            except SystemExit:
                pass  # Expected when exiting
            
            # Verify invalid option message was printed
            mock_print.assert_any_call("\nInvalid option. Please try again.")

    @patch('sys.argv', ['ebookstore.py', '--database-file', 'test.db'])
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_value_error_handling(self, mock_print, mock_input):
        """Test handling of ValueError exceptions."""
        # Mock user inputs that cause ValueError
        mock_input.side_effect = [
            '1',  # Select "Enter book"
            '',   # Empty title (will cause ValueError)
            '',   # Empty title again
            '',   # Empty title third time (max attempts)
            '',   # Return to menu
            '0'   # Exit
        ]
        
        with patch('ebookstore.BookStoreSqlite') as mock_bookstore_class:
            mock_bookstore = MagicMock()
            mock_bookstore_class.return_value = mock_bookstore
            
            # Mock get_book to raise ValueError
            with patch('ebookstore.get_book') as mock_get_book:
                mock_get_book.side_effect = ValueError("Test error message")
                
                try:
                    ebookstore.main()
                except SystemExit:
                    pass  # Expected when exiting
                
                # Verify error was handled and printed
                # Check that the error message was printed 
                # (the application prints exception objects)
                error_found = False
                for call_args in mock_print.call_args_list:
                    # Check if this call contains the error message
                    if len(call_args[0]) >= 2 and (
                        isinstance(call_args[0][1], ValueError)
                    ):
                        if "Test error message" in str(call_args[0][1]):
                            error_found = True
                            break
                
                self.assertTrue(
                    error_found, 
                    "ValueError with 'Test error message' was not printed"
                )

    @patch(
            'sys.argv', 
            ['ebookstore.py', '--connection-url', 'mysql://user:pass@host/db']
    )
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_mysql_connection(self, mock_print, mock_input):
        """Test main function with MySQL connection."""
        mock_input.side_effect = ['0']  # Exit immediately
        
        with patch('ebookstore.BookStoreMySQL') as mock_mysql_class:
            mock_mysql = MagicMock()
            mock_mysql_class.return_value = mock_mysql
            
            try:
                ebookstore.main()
            except SystemExit:
                pass  # Expected when exiting
            
            # Verify MySQL bookstore was created
            mock_mysql_class.assert_called_once()

    @patch(
            'sys.argv', 
            [
                'ebookstore.py', 
                '--database-file', 
                'test.db', 
                '--table-records', 
                'records.csv'
            ]
    )
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_with_table_records(self, mock_print, mock_input):
        """Test main function with table records file."""
        mock_input.side_effect = ['0']  # Exit immediately
        
        with patch('ebookstore.get_table_records') as mock_get_records:
            with patch('ebookstore.BookStoreSqlite') as mock_bookstore_class:
                mock_bookstore = MagicMock()
                mock_bookstore_class.return_value = mock_bookstore
                
                try:
                    ebookstore.main()
                except SystemExit:
                    pass  # Expected when exiting
                
                # Verify get_table_records was called
                mock_get_records.assert_called_once()

    @patch('sys.argv', ['ebookstore.py'])
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_no_database_connection(self, mock_print, mock_input):
        """Test main function with no database connection provided."""
        with patch('ebookstore.get_database_connection') as mock_get_conn:
            # Simulate exit due to no connection
            mock_get_conn.side_effect = SystemExit(1)  
            
            with self.assertRaises(SystemExit):
                ebookstore.main()

    @patch(
            'sys.argv', 
            ['ebookstore.py', '--database-file', '/invalid/path/test.db']
    )
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_permission_error(self, mock_print, mock_input):
        """Test main function with permission error."""
        with patch('os.makedirs') as mock_makedirs:
            mock_makedirs.side_effect = PermissionError("Permission denied")
            
            with self.assertRaises(SystemExit):
                ebookstore.main()

    def test_real_sqlite_database_operations(self):
        """Test actual database operations with real SQLite database."""
        with patch('builtins.print'):
            # Create a real BookStore instance
            bookstore = BookStoreSqlite(self.db_path)
            
            # Test inserting a book
            from classes import Book
            test_book = Book("Integration Test Book", "Integration Author", 25)
            bookstore.insert_book(test_book)
            
            # Verify book was inserted
            book_info = {
                "title": "Integration Test Book", 
                "author": "Integration Author"
            }
            result = bookstore.find_book(book_info)
            self.assertIsNotNone(result)
            self.assertEqual(result[1], "Integration Test Book")
            self.assertEqual(result[2], "Integration Author")
            self.assertEqual(result[3], 25)
            
            # Test updating the book
            book_id = result[0]
            update_info = {
                "id": book_id,
                "field": "quantity",
                "action": "add",
                "qty": 5
            }
            bookstore.update_book(update_info)
            
            # Verify quantity was updated
            result = bookstore.find_book({"id": book_id})
            self.assertEqual(result[3], 30)  # 25 + 5
            
            # Test searching
            with patch('builtins.print'):
                bookstore.search_books("Integration")
            
            # Test deleting the book
            bookstore.delete_book({"id": book_id})
            
            # Verify book was deleted
            result = bookstore.find_book({"id": book_id})
            self.assertIsNone(result)
            
            bookstore.db.close()

    def test_edge_cases_and_error_conditions(self):
        """Test various edge cases and error conditions."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.db_path)
            
            # Test updating non-existent book
            book_info = {
                "id": 99999,
                "field": "quantity",
                "action": "set",
                "qty": 10
            }
            with patch('builtins.print') as mock_print:
                bookstore.update_book(book_info)
                mock_print.assert_any_call("\nBook not found")
            
            # Test deleting non-existent book
            with patch('builtins.print') as mock_print:
                bookstore.delete_book({"id": 99999})
                mock_print.assert_any_call("\nBook not found")
            
            # Test searching for non-existent book
            with patch('builtins.print') as mock_print:
                bookstore.search_books("NonExistentBook12345")
                mock_print.assert_any_call("\nBook not found")
            
            # Test quantity subtraction that would result in negative
            from classes import Book
            test_book = Book("Test Book", "Test Author", 5)
            bookstore.insert_book(test_book)
            
            book_info_search = {"title": "Test Book", "author": "Test Author"}
            result = bookstore.find_book(book_info_search)
            book_id = result[0]
            
            # Try to subtract more than available
            book_info = {
                "id": book_id,
                "field": "quantity",
                "action": "sub",
                "qty": 10  # More than the 5 available
            }
            
            with self.assertRaises(Exception) as context:
                bookstore.update_book(book_info)
            
            self.assertIn(
                "You can't perform this operation", str(context.exception)
            )
            
            bookstore.db.close()


class TestCommandLineArguments(unittest.TestCase):
    """Test command-line argument parsing and validation."""

    def test_database_file_argument(self):
        """Test --database-file argument parsing."""
        with patch('sys.argv', ['ebookstore.py', '--database-file', 'mydb.db']):
            from functions import parse_cli_args
            args = parse_cli_args()
            self.assertEqual(args.database_file, 'mydb.db')

    def test_connection_url_argument(self):
        """Test --connection-url argument parsing."""
        url = 'mysql://user:pass@localhost:3306/testdb'
        with patch('sys.argv', ['ebookstore.py', '--connection-url', url]):
            from functions import parse_cli_args
            args = parse_cli_args()
            self.assertEqual(args.connection_url, url)

    def test_table_records_argument(self):
        """Test --table-records argument parsing."""
        with patch(
            'sys.argv', 
            [
                'ebookstore.py', 
                '--database-file', 
                'test.db', 
                '--table-records', 
                'records.csv'
                ]
        ):
            from functions import parse_cli_args
            args = parse_cli_args()
            self.assertEqual(args.table_records, 'records.csv')

    def test_table_name_argument(self):
        """Test --table-name argument parsing."""
        with patch(
            'sys.argv', 
            [
                'ebookstore.py', 
                '--database-file', 
                'test.db', 
                '--table-name', 
                'custom_books'
            ]
        ):
            from functions import parse_cli_args
            args = parse_cli_args()
            self.assertEqual(args.table_name, 'custom_books')

    def test_all_arguments_together(self):
        """Test all arguments together."""
        argv = [
            'ebookstore.py',
            '--connection-url', 'mysql://user:pass@host/db',
            '--table-records', 'records.csv',
            '--table-name', 'my_books'
        ]
        with patch('sys.argv', argv):
            from functions import parse_cli_args
            args = parse_cli_args()
            self.assertEqual(args.connection_url, 'mysql://user:pass@host/db')
            self.assertEqual(args.table_records, 'records.csv')
            self.assertEqual(args.table_name, 'my_books')


class TestFileOperations(unittest.TestCase):
    """Test file operations and CSV handling."""

    def test_csv_file_reading(self):
        """Test reading CSV file with table records."""
        csv_content = (
            "id,title,author,qty\n"
            "1,\"Test Book 1\",\"Author 1\",10\n"
            "2,\"Test Book 2\",\"Author 2\",20\n"
            "3,\"Book with, comma\",\"Author, Name\",30"
        )
        
        with tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix='.csv'
        ) as temp_file:
            temp_file.write(csv_content)
            temp_file_path = temp_file.name
        
        try:
            from functions import get_table_records
            table_records = []
            get_table_records(table_records, temp_file_path)
            
            expected = [
                ('1', 'Test Book 1', 'Author 1', '10'),
                ('2', 'Test Book 2', 'Author 2', '20'),
                ('3', 'Book with, comma', 'Author, Name', '30')
            ]
            self.assertEqual(table_records, expected)
        finally:
            os.unlink(temp_file_path)

    def test_directory_creation(self):
        """Test directory creation for database file."""
        temp_dir = tempfile.mkdtemp()
        try:
            nested_path = os.path.join(
                temp_dir, 'subdir1', 'subdir2', 'test.db'
            )
            
            # This should create the nested directories
            if os.path.dirname(nested_path):
                os.makedirs(os.path.dirname(nested_path), exist_ok=True)
            
            # Verify directories were created
            self.assertTrue(os.path.exists(os.path.dirname(nested_path)))
        finally:
            import shutil
            shutil.rmtree(temp_dir)


if __name__ == '__main__':
    # Capture stdout to avoid cluttering test output
    unittest.main(verbosity=2)
