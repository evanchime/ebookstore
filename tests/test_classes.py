"""
Unit and integration tests for BookStore classes (SQLite and MySQL).
Tests database operations, error handling, and data validation.
"""

import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
import sys

# Add parent directory to path to import application modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes import Book, BookStoreSqlite, BookStoreMySQL
from abstract_classes import BookStore


class TestBookStoreSqlite(unittest.TestCase):
    """Test cases for BookStoreSqlite class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        
        # Test data
        self.test_book = Book("Test Title", "Test Author", 10)
        self.test_records = [
            (1, "Book 1", "Author 1", 5),
            (2, "Book 2", "Author 2", 15)
        ]

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_bookstore_sqlite_initialization(self):
        """Test successful BookStoreSqlite initialization."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.db_path)
            
            self.assertEqual(bookstore.table_name, 'book')
            self.assertIsNotNone(bookstore.db)
            self.assertIsNotNone(bookstore.cursor)
            
            # Verify table was created
            bookstore.cursor.execute(
                "SELECT name "
                "FROM sqlite_master "
                "WHERE type='table' "
                "AND name='book'"
            )
            result = bookstore.cursor.fetchone()
            self.assertIsNotNone(result)
            
            bookstore.db.close()

    def test_bookstore_sqlite_custom_table_name(self):
        """Test BookStoreSqlite initialization with custom table name."""
        custom_table = "custom_books"
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.db_path, custom_table)
            
            self.assertEqual(bookstore.table_name, custom_table)
            
            # Verify custom table was created
            bookstore.cursor.execute(
                "SELECT name "
                "FROM sqlite_master "
                "WHERE type='table' "
                f"AND name='{custom_table}'"
            )
            result = bookstore.cursor.fetchone()
            self.assertIsNotNone(result)
            
            bookstore.db.close()

    def test_bookstore_sqlite_with_predefined_records(self):
        """Test BookStoreSqlite initialization with predefined 
        records."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(
                self.db_path, table_records=self.test_records
            )
            
            # Verify records were inserted
            bookstore.cursor.execute("SELECT COUNT(*) FROM book")
            count = bookstore.cursor.fetchone()[0]
            self.assertEqual(count, 2)
            
            bookstore.db.close()

    def test_unicode_nocase_collation(self):
        """Test unicode case-insensitive collation."""
        # Test equal strings with different cases
        result = BookStoreSqlite.unicode_nocase_collation("Test", "test")
        self.assertEqual(result, 0)
        
        # Test less than
        result = BookStoreSqlite.unicode_nocase_collation("apple", "banana")
        self.assertEqual(result, -1)
        
        # Test greater than
        result = BookStoreSqlite.unicode_nocase_collation("zebra", "apple")
        self.assertEqual(result, 1)

    def test_insert_book_success(self):
        """Test successful book insertion."""
        with patch('builtins.print') as mock_print:
            bookstore = BookStoreSqlite(self.db_path)
            bookstore.insert_book(self.test_book)
            
            # Verify book was inserted
            bookstore.cursor.execute(
                "SELECT * FROM book WHERE title = ? AND author = ?", 
                (self.test_book.title, self.test_book.author)
            )
            result = bookstore.cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[1], self.test_book.title)
            self.assertEqual(result[2], self.test_book.author)
            self.assertEqual(result[3], self.test_book.qty)
            
            # Check if success message was printed
            mock_print.assert_any_call(
                f"\nBook entered with id: {bookstore.cursor.lastrowid}"
            )
            
            bookstore.db.close()

    def test_insert_book_duplicate(self):
        """Test inserting duplicate book."""
        with patch('builtins.print') as mock_print:
            bookstore = BookStoreSqlite(self.db_path)
            
            # Insert book twice
            bookstore.insert_book(self.test_book)
            bookstore.insert_book(self.test_book)
            
            # Verify only one record exists
            bookstore.cursor.execute(
                "SELECT COUNT(*) FROM book WHERE title = ? AND author = ?", 
                (self.test_book.title, self.test_book.author)
            )
            count = bookstore.cursor.fetchone()[0]
            self.assertEqual(count, 1)
            
            # Check if duplicate message was printed
            mock_print.assert_any_call("\nBook already exists")
            
            bookstore.db.close()

    def test_find_book_by_id(self):
        """Test finding book by ID."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.db_path)
            bookstore.insert_book(self.test_book)
            
            # Get the inserted book's ID
            bookstore.cursor.execute(
                "SELECT id FROM book WHERE title = ? AND author = ?", 
                (self.test_book.title, self.test_book.author)
            )
            book_id = bookstore.cursor.fetchone()[0]
            
            # Find book by ID
            book_info = {"id": book_id}
            result = bookstore.find_book(book_info)
            
            self.assertIsNotNone(result)
            self.assertEqual(result[0], book_id)
            self.assertEqual(result[1], self.test_book.title)
            
            bookstore.db.close()

    def test_find_book_by_title_author(self):
        """Test finding book by title and author."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.db_path)
            bookstore.insert_book(self.test_book)
            
            # Find book by title and author
            book_info = {
                "title": self.test_book.title, 
                "author": self.test_book.author
            }
            result = bookstore.find_book(book_info)
            
            self.assertIsNotNone(result)
            self.assertEqual(result[1], self.test_book.title)
            self.assertEqual(result[2], self.test_book.author)
            
            bookstore.db.close()

    def test_find_book_not_found(self):
        """Test finding non-existent book."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.db_path)
            
            book_info = {"title": "Non-existent", "author": "Unknown"}
            result = bookstore.find_book(book_info)
            
            self.assertIsNone(result)
            
            bookstore.db.close()

    def test_delete_book_by_id_success(self):
        """Test successful book deletion by ID."""
        with patch('builtins.print') as mock_print:
            bookstore = BookStoreSqlite(self.db_path)
            bookstore.insert_book(self.test_book)
            
            # Get the inserted book's ID
            bookstore.cursor.execute(
                "SELECT id FROM book WHERE title = ? AND author = ?", 
                (self.test_book.title, self.test_book.author)
            )
            book_id = bookstore.cursor.fetchone()[0]
            
            # Delete book by ID
            book_info = {"id": book_id}
            bookstore.delete_book(book_info)
            
            # Verify book was deleted
            result = bookstore.find_book(book_info)
            self.assertIsNone(result)
            
            mock_print.assert_any_call("\nBook deleted successfully")
            
            bookstore.db.close()

    def test_delete_book_by_title_author_success(self):
        """Test successful book deletion by title and author."""
        with patch('builtins.print') as mock_print:
            bookstore = BookStoreSqlite(self.db_path)
            bookstore.insert_book(self.test_book)
            
            # Delete book by title and author
            book_info = {
                "title": self.test_book.title, 
                "author": self.test_book.author
            }
            bookstore.delete_book(book_info)
            
            # Verify book was deleted
            result = bookstore.find_book(book_info)
            self.assertIsNone(result)
            
            mock_print.assert_any_call("\nBook deleted successfully")
            
            bookstore.db.close()

    def test_delete_book_not_found(self):
        """Test deleting non-existent book."""
        with patch('builtins.print') as mock_print:
            bookstore = BookStoreSqlite(self.db_path)
            
            book_info = {"title": "Non-existent", "author": "Unknown"}
            bookstore.delete_book(book_info)
            
            mock_print.assert_any_call("\nBook not found")
            
            bookstore.db.close()

    def test_search_books_found(self):
        """Test searching books with results."""
        with patch('builtins.print') as mock_print:
            bookstore = BookStoreSqlite(
                self.db_path, table_records=self.test_records
            )
            
            # Search for existing book
            bookstore.search_books("Book 1")
            
            # Verify tabulated output was printed (we can't easily test 
            # the exact output)
            self.assertTrue(mock_print.called)
            
            bookstore.db.close()

    def test_search_books_not_found(self):
        """Test searching books with no results."""
        with patch('builtins.print') as mock_print:
            bookstore = BookStoreSqlite(self.db_path)
            
            bookstore.search_books("Non-existent")
            
            mock_print.assert_any_call("\nBook not found")
            
            bookstore.db.close()

    def test_search_books_by_author(self):
        """Test searching books by author."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(
                self.db_path, table_records=self.test_records
            )
            
            # Search by author should find books
            bookstore.cursor.execute(
                "SELECT * FROM book WHERE author LIKE ?", ('%Author 1%',)
            )
            result = bookstore.cursor.fetchall()
            self.assertEqual(len(result), 1)
            
            bookstore.db.close()

    def test_update_qty_utility_by_id(self):
        """Test updating quantity by book ID."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.db_path)
            bookstore.insert_book(self.test_book)
            
            # Get book ID
            bookstore.cursor.execute(
                "SELECT id FROM book WHERE title = ? AND author = ?", 
                (self.test_book.title, self.test_book.author)
            )
            book_id = bookstore.cursor.fetchone()[0]
            
            # Update quantity
            book_info = {"id": book_id}
            new_qty = 25
            bookstore.update_qty_utility(new_qty, book_info)
            bookstore.db.commit()
            
            # Verify quantity was updated
            result = bookstore.find_book(book_info)
            self.assertEqual(result[3], new_qty)
            
            bookstore.db.close()

    def test_update_qty_utility_by_title_author(self):
        """Test updating quantity by title and author."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.db_path)
            bookstore.insert_book(self.test_book)
            
            # Update quantity
            book_info = {
                "title": self.test_book.title, 
                "author": self.test_book.author
            }
            new_qty = 30
            bookstore.update_qty_utility(new_qty, book_info)
            bookstore.db.commit()
            
            # Verify quantity was updated
            result = bookstore.find_book(book_info)
            self.assertEqual(result[3], new_qty)
            
            bookstore.db.close()

    def test_update_title_utility_by_id(self):
        """Test updating title by book ID."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.db_path)
            bookstore.insert_book(self.test_book)
            
            # Get book ID
            bookstore.cursor.execute(
                "SELECT id FROM book WHERE title = ? AND author = ?", 
                (self.test_book.title, self.test_book.author)
            )
            book_id = bookstore.cursor.fetchone()[0]
            
            # Update title
            new_title = "Updated Title"
            book_info = {"id": book_id, "new_title": new_title}
            bookstore.update_title_utility(book_info)
            bookstore.db.commit()
            
            # Verify title was updated
            result = bookstore.find_book({"id": book_id})
            self.assertEqual(result[1], new_title)
            
            bookstore.db.close()

    def test_update_author_utility_by_id(self):
        """Test updating author by book ID."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.db_path)
            bookstore.insert_book(self.test_book)
            
            # Get book ID
            bookstore.cursor.execute(
                "SELECT id FROM book WHERE title = ? AND author = ?", 
                (self.test_book.title, self.test_book.author)
            )
            book_id = bookstore.cursor.fetchone()[0]
            
            # Update author
            new_author = "Updated Author"
            book_info = {"id": book_id, "new_author": new_author}
            bookstore.update_author_utility(book_info)
            bookstore.db.commit()
            
            # Verify author was updated
            result = bookstore.find_book({"id": book_id})
            self.assertEqual(result[2], new_author)
            
            bookstore.db.close()

    def test_database_error_handling(self):
        """Test database error handling."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.db_path)
            
            # Manually close the database to cause an error
            bookstore.db.close()
            
            # Try to insert a book, which should cause an error
            with self.assertRaises(Exception):
                bookstore.insert_book(self.test_book)

    def test_case_insensitive_search(self):
        """Test case-insensitive search functionality."""
        with patch('builtins.print'):
            bookstore = BookStoreSqlite(self.db_path)
            test_book = Book("The Great Gatsby", "F. Scott Fitzgerald", 5)
            bookstore.insert_book(test_book)
            
            # Search with different cases
            bookstore.cursor.execute(
                "SELECT * FROM book WHERE title LIKE ? COLLATE UNICODE_NOCASE", 
                ('%great gatsby%',)
            )
            result = bookstore.cursor.fetchall()
            self.assertEqual(len(result), 1)
            
            bookstore.db.close()


class TestBookStoreMySQL(unittest.TestCase):
    """Test cases for BookStoreMySQL class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.db_params = {
            'host': 'localhost',
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_pass',
            'port': '3306'
        }
        self.test_book = Book("Test Title", "Test Author", 10)

    @patch('mysql.connector.connect')
    @patch('builtins.print')
    def test_bookstore_mysql_initialization(self, mock_print, mock_connect):
        """Test successful BookStoreMySQL initialization."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        
        bookstore = BookStoreMySQL(self.db_params)
        
        self.assertEqual(bookstore.table_name, 'book')
        mock_connect.assert_called_once_with(
            host='localhost',
            database='test_db',
            user='test_user',
            password='test_pass',
            port='3306'
        )
        mock_cursor.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('mysql.connector.connect')
    @patch('builtins.print')
    def test_bookstore_mysql_custom_table(self, mock_print, mock_connect):
        """Test BookStoreMySQL initialization with custom table name."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        
        custom_table = "custom_books"
        bookstore = BookStoreMySQL(self.db_params, custom_table)
        
        self.assertEqual(bookstore.table_name, custom_table)

    @patch('mysql.connector.connect')
    @patch('builtins.print')
    def test_insert_book_mysql_success(self, mock_print, mock_connect):
        """Test successful book insertion in MySQL."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # Book doesn't exist
        mock_cursor.lastrowid = 123
        
        bookstore = BookStoreMySQL(self.db_params)
        bookstore.insert_book(self.test_book)
        
        # Verify insert was called
        insert_calls = [
            arg for arg in mock_cursor.execute.call_args_list 
            if 'INSERT INTO' in str(arg)
        ]
        self.assertTrue(len(insert_calls) > 0)
        mock_print.assert_any_call("\nBook entered with id: 123")

    @patch('mysql.connector.connect')
    @patch('builtins.print')
    def test_insert_book_mysql_duplicate(self, mock_print, mock_connect):
        """Test inserting duplicate book in MySQL."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        # Book exists
        mock_cursor.fetchone.return_value = (1, "Test Title", "Test Author", 10)  
        
        bookstore = BookStoreMySQL(self.db_params)
        bookstore.insert_book(self.test_book)
        
        mock_print.assert_any_call("\nBook already exists")

    @patch('mysql.connector.connect')
    @patch('builtins.print')
    def test_find_book_mysql_by_id(self, mock_print, mock_connect):
        """Test finding book by ID in MySQL."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, "Test Title", "Test Author", 10)
        
        bookstore = BookStoreMySQL(self.db_params)
        book_info = {"id": 1}
        result = bookstore.find_book(book_info)
        
        self.assertEqual(result, (1, "Test Title", "Test Author", 10))

    @patch('mysql.connector.connect')
    @patch('builtins.print')
    def test_delete_book_mysql_success(self, mock_print, mock_connect):
        """Test successful book deletion in MySQL."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, "Test Title", "Test Author", 10)
        
        bookstore = BookStoreMySQL(self.db_params)
        book_info = {"id": 1}
        bookstore.delete_book(book_info)
        
        mock_print.assert_any_call("\nBook deleted successfully")

    @patch('mysql.connector.connect')
    @patch('builtins.print')
    def test_search_books_mysql_found(self, mock_print, mock_connect):
        """Test searching books with results in MySQL."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "Test Title", "Test Author", 10)
        ]
        
        bookstore = BookStoreMySQL(self.db_params)
        bookstore.search_books("Test")
        
        # Verify search was executed
        search_calls = [
            arg for arg in mock_cursor.execute.call_args_list 
            if 'SELECT * FROM' in str(arg) and 'LIKE' in str(arg)
        ]
        self.assertTrue(len(search_calls) > 0)

    @patch('mysql.connector.connect')
    @patch('builtins.print')
    def test_search_books_mysql_not_found(self, mock_print, mock_connect):
        """Test searching books with no results in MySQL."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        bookstore = BookStoreMySQL(self.db_params)
        bookstore.search_books("Non-existent")
        
        mock_print.assert_any_call("\nBook not found")

    @patch('mysql.connector.connect')
    @patch('builtins.print')
    def test_mysql_connection_with_default_port(self, mock_print, mock_connect):
        """Test MySQL connection without explicit port."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        
        db_params_no_port = {
            'host': 'localhost',
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_pass'
        }
        
        BookStoreMySQL(db_params_no_port)
        
        mock_connect.assert_called_once_with(
            host='localhost',
            database='test_db',
            user='test_user',
            password='test_pass',
            port=3306  # Default port should be used
        )


class TestAbstractBookStore(unittest.TestCase):
    """Test cases for abstract BookStore methods."""

    def test_get_update_qty_utility_add(self):
        """Test quantity update utility with add action."""
        book_info = {"action": "add", "qty": 5}
        record = (1, "Title", "Author", 10)  # Current qty is 10
        
        result = BookStore.get_update_qty_utility(book_info, record)
        self.assertEqual(result, 15)  # 10 + 5

    def test_get_update_qty_utility_sub(self):
        """Test quantity update utility with subtract action."""
        book_info = {"action": "sub", "qty": 3}
        record = (1, "Title", "Author", 10)  # Current qty is 10
        
        result = BookStore.get_update_qty_utility(book_info, record)
        self.assertEqual(result, 7)  # 10 - 3

    def test_get_update_qty_utility_set(self):
        """Test quantity update utility with set action."""
        book_info = {"action": "set", "qty": 20}
        record = (1, "Title", "Author", 10)  # Current qty is 10
        
        result = BookStore.get_update_qty_utility(book_info, record)
        self.assertEqual(result, 20)  # Set to 20

    def test_get_update_qty_utility_negative_result(self):
        """Test quantity update utility with negative result."""
        book_info = {"action": "sub", "qty": 15}
        record = (1, "Title", "Author", 10)  # Current qty is 10
        
        with self.assertRaises(Exception) as context:
            BookStore.get_update_qty_utility(book_info, record)
        
        self.assertIn(
            "You can't perform this operation", str(context.exception)
        )
        self.assertIn(
            "You only have 10 of this book in stock", str(context.exception)
        )

    @patch('builtins.print')
    def test_update_book_integration(self, mock_print):
        """Test complete update_book workflow with SQLite."""
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        try:
            bookstore = BookStoreSqlite(temp_db.name)
            test_book = Book("Original Title", "Original Author", 10)
            bookstore.insert_book(test_book)
            
            # Get book ID
            bookstore.cursor.execute(
                "SELECT id FROM book WHERE title = ? AND author = ?", 
                (test_book.title, test_book.author)
            )
            book_id = bookstore.cursor.fetchone()[0]
            
            # Test quantity update
            book_info = {
                "id": book_id,
                "field": "quantity",
                "action": "add",
                "qty": 5
            }
            bookstore.update_book(book_info)
            
            # Verify quantity was updated
            result = bookstore.find_book({"id": book_id})
            self.assertEqual(result[3], 15)  # 10 + 5
            
            mock_print.assert_any_call("\nBook updated successfully")
            
            bookstore.db.close()
        finally:
            if os.path.exists(temp_db.name):
                os.unlink(temp_db.name)


if __name__ == '__main__':
    unittest.main()
