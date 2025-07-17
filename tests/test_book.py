"""
Unit tests for the Book class.
Tests basic book functionality and data validation.
"""

import unittest
import sys
import os

# Add parent directory to path to import application modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes import Book


class TestBook(unittest.TestCase):
    """Test cases for the Book class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_title = "Test Book"
        self.test_author = "Test Author"
        self.test_qty = 10

    def test_book_creation_valid_data(self):
        """Test creating a book with valid data."""
        book = Book(self.test_title, self.test_author, self.test_qty)
        
        self.assertEqual(book.title, self.test_title)
        self.assertEqual(book.author, self.test_author)
        self.assertEqual(book.qty, self.test_qty)

    def test_book_creation_with_spaces_in_title(self):
        """Test creating a book with spaces in title - spaces should be stripped."""
        title_with_spaces = "  A Tale of Two Cities  "
        book = Book(title_with_spaces, self.test_author, self.test_qty)
        
        self.assertEqual(book.title, "A Tale of Two Cities")  # Spaces stripped
        self.assertEqual(book.author, self.test_author)
        self.assertEqual(book.qty, self.test_qty)

    def test_book_creation_with_unicode_characters(self):
        """Test creating a book with unicode characters."""
        unicode_title = "Café de l'Ésötérique"
        unicode_author = "François Dürrenmatţ"
        book = Book(unicode_title, unicode_author, self.test_qty)
        
        self.assertEqual(book.title, unicode_title)
        self.assertEqual(book.author, unicode_author)
        self.assertEqual(book.qty, self.test_qty)

    def test_book_creation_empty_title(self):
        """Test creating a book with empty title raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Book("", self.test_author, self.test_qty)
        
        self.assertIn("Title cannot be empty", str(context.exception))

    def test_book_creation_empty_author(self):
        """Test creating a book with empty author raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Book(self.test_title, "", self.test_qty)
        
        self.assertIn("Author cannot be empty", str(context.exception))

    def test_book_creation_whitespace_only_title(self):
        """Test creating a book with whitespace-only title raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Book("   ", self.test_author, self.test_qty)
        
        self.assertIn("Title cannot be empty", str(context.exception))

    def test_book_creation_whitespace_only_author(self):
        """Test creating a book with whitespace-only author raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Book(self.test_title, "   ", self.test_qty)
        
        self.assertIn("Author cannot be empty", str(context.exception))

    def test_book_creation_non_integer_quantity(self):
        """Test creating a book with non-integer quantity raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Book(self.test_title, self.test_author, "10")
        
        self.assertIn("Quantity must be an integer", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            Book(self.test_title, self.test_author, 10.5)
        
        self.assertIn("Quantity must be an integer", str(context.exception))

    def test_book_creation_negative_quantity_validation(self):
        """Test creating a book with negative quantity raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Book(self.test_title, self.test_author, -1)
        
        self.assertIn("Quantity cannot be negative", str(context.exception))

    def test_book_creation_zero_quantity(self):
        """Test creating a book with zero quantity."""
        book = Book(self.test_title, self.test_author, 0)
        
        self.assertEqual(book.title, self.test_title)
        self.assertEqual(book.author, self.test_author)
        self.assertEqual(book.qty, 0)

    def test_book_creation_negative_quantity(self):
        """Test creating a book with negative quantity raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Book(self.test_title, self.test_author, -5)
        
        self.assertIn("Quantity cannot be negative", str(context.exception))

    def test_book_creation_large_quantity(self):
        """Test creating a book with very large quantity."""
        large_qty = 999999
        book = Book(self.test_title, self.test_author, large_qty)
        
        self.assertEqual(book.title, self.test_title)
        self.assertEqual(book.author, self.test_author)
        self.assertEqual(book.qty, large_qty)

    def test_book_attributes_modification(self):
        """Test modifying book attributes after creation."""
        book = Book(self.test_title, self.test_author, self.test_qty)
        
        # Modify attributes
        book.title = "Modified Title"
        book.author = "Modified Author"
        book.qty = 20
        
        self.assertEqual(book.title, "Modified Title")
        self.assertEqual(book.author, "Modified Author")
        self.assertEqual(book.qty, 20)

    def test_book_creation_with_special_characters(self):
        """Test creating a book with special characters in title and author."""
        special_title = "Title with @#$%^&*()_+{}|:<>?[]\\;'\",./"
        special_author = "Author with ñáéíóú çÇ"
        book = Book(special_title, special_author, self.test_qty)
        
        self.assertEqual(book.title, special_title)
        self.assertEqual(book.author, special_author)
        self.assertEqual(book.qty, self.test_qty)

    def test_book_creation_with_numeric_strings(self):
        """Test creating a book with numeric strings."""
        numeric_title = "12345"
        numeric_author = "67890"
        book = Book(numeric_title, numeric_author, self.test_qty)
        
        self.assertEqual(book.title, numeric_title)
        self.assertEqual(book.author, numeric_author)
        self.assertEqual(book.qty, self.test_qty)


if __name__ == '__main__':
    unittest.main()
