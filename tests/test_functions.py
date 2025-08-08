"""
Unit tests for the functions module.
Tests all utility functions for input validation and processing.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import tempfile

# Add parent directory to path to import application modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions import (
    get_book_title_utility, get_book_author_utility, get_book_qty_utility,
    get_update_field_utility, get_qty_action_utility, get_book_info,
    get_book, get_book_update_info, get_book_search_query,
    get_database_connection_params, get_table_records, parse_cli_args,
    get_database_connection, exit_utility, return_to_menu,
    get_book_id_utility, do_you_have_book_id_utility
)
from classes import Book, BookStoreSqlite, BookStoreMySQL


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions."""

    @patch('builtins.input')
    def test_get_book_id_utility_valid_input(self, mock_input):
        """Test get_book_id_utility with valid input."""
        mock_input.return_value = "123"
        result = get_book_id_utility()
        self.assertEqual(result, 123)

    @patch('builtins.input')
    def test_get_book_id_utility_invalid_then_valid(self, mock_input):
        """Test get_book_id_utility with invalid then valid input."""
        mock_input.side_effect = ["0", "abc", "456"]
        with patch('builtins.print'):
            result = get_book_id_utility()
            self.assertEqual(result, 456)

    @patch('builtins.input')
    def test_get_book_id_utility_max_attempts_exceeded(self, mock_input):
        """Test get_book_id_utility when max attempts exceeded."""
        mock_input.side_effect = ["0", "abc", "-5"]
        with patch('builtins.print'):
            with self.assertRaises(ValueError) as context:
                get_book_id_utility()
            self.assertIn(
                "Aborting...book id must be whole number greater than 0", 
                str(context.exception)
            )

    @patch('builtins.input')
    def test_do_you_have_book_id_utility_yes(self, mock_input):
        """Test do_you_have_book_id_utility with 'yes' input."""
        mock_input.return_value = "yes"
        result = do_you_have_book_id_utility()
        self.assertEqual(result, "yes")

    @patch('builtins.input')
    def test_do_you_have_book_id_utility_no(self, mock_input):
        """Test do_you_have_book_id_utility with 'no' input."""
        mock_input.return_value = "no"
        result = do_you_have_book_id_utility()
        self.assertEqual(result, "no")

    @patch('builtins.input')
    def test_do_you_have_book_id_utility_case_insensitive(self, mock_input):
        """Test do_you_have_book_id_utility with case variations."""
        test_cases = ["YES", "No", "yEs", "NO"]
        expected = ["yes", "no", "yes", "no"]
        
        for input_val, expected_val in zip(test_cases, expected):
            mock_input.return_value = input_val
            result = do_you_have_book_id_utility()
            self.assertEqual(result, expected_val)

    @patch('builtins.input')
    def test_do_you_have_book_id_utility_invalid_input(self, mock_input):
        """Test do_you_have_book_id_utility with invalid input."""
        mock_input.side_effect = ["maybe", "sure", "absolutely"]
        with patch('builtins.print'):
            with self.assertRaises(ValueError) as context:
                do_you_have_book_id_utility()
            self.assertIn(
                "Aborting...you must enter 'yes' or 'no'", 
                str(context.exception)
            )

    @patch('builtins.input')
    def test_get_book_title_utility_valid_input(self, mock_input):
        """Test get_book_title_utility with valid input."""
        mock_input.return_value = "Test Book Title"
        result = get_book_title_utility()
        self.assertEqual(result, "Test book title")

    @patch('builtins.input')
    def test_get_book_title_utility_with_extra_spaces(self, mock_input):
        """Test get_book_title_utility with extra spaces."""
        mock_input.return_value = "Test   Book    Title"
        result = get_book_title_utility()
        self.assertEqual(result, "Test book title")

    @patch('builtins.input')
    def test_get_book_title_utility_empty_input(self, mock_input):
        """Test get_book_title_utility with empty input."""
        mock_input.side_effect = ["", "  ", "Valid Title"]
        with patch('builtins.print'):
            result = get_book_title_utility()
            self.assertEqual(result, "Valid title")

    @patch('builtins.input')
    def test_get_book_title_utility_max_attempts_exceeded(self, mock_input):
        """Test get_book_title_utility when max attempts exceeded."""
        mock_input.side_effect = ["", "  ", "   "]
        with patch('builtins.print'):
            with self.assertRaises(ValueError) as context:
                get_book_title_utility()
            self.assertIn(
                "Aborting...title cannot be empty", 
                str(context.exception)
            )

    @patch('builtins.input')
    def test_get_book_title_utility_new_title(self, mock_input):
        """Test get_book_title_utility with new_title parameter."""
        mock_input.return_value = "New Title"
        result = get_book_title_utility("new title")
        self.assertEqual(result, "New title")

    @patch('builtins.input')
    def test_get_book_title_utility_capitalization_behavior(self, mock_input):
        """Test get_book_title_utility capitalization behavior with various inputs."""
        # Test different capitalization scenarios
        test_cases = [
            ("lowercase title", "Lowercase title"),
            ("UPPERCASE TITLE", "Uppercase title"),
            ("MiXeD cAsE tItLe", "Mixed case title"),
            ("iOS Programming Guide", "Ios programming guide"),
            ("the great gatsby", "The great gatsby"),
            ("harry potter and the philosopher's stone", "Harry potter and the philosopher's stone")
        ]
        
        for input_title, expected_output in test_cases:
            with self.subTest(input_title=input_title):
                mock_input.return_value = input_title
                result = get_book_title_utility()
                self.assertEqual(result, expected_output)

    @patch('builtins.input')
    def test_get_book_author_utility_valid_input(self, mock_input):
        """Test get_book_author_utility with valid input."""
        mock_input.return_value = "Test Author"
        result = get_book_author_utility()
        self.assertEqual(result, "TEST AUTHOR")

    @patch('builtins.input')
    def test_get_book_author_utility_with_extra_spaces(self, mock_input):
        """Test get_book_author_utility with extra spaces."""
        mock_input.return_value = "Test   Author   Name"
        result = get_book_author_utility()
        self.assertEqual(result, "TEST AUTHOR NAME")

    @patch('builtins.input')
    def test_get_book_author_utility_empty_input(self, mock_input):
        """Test get_book_author_utility with empty input."""
        mock_input.side_effect = ["", "Valid Author"]
        with patch('builtins.print'):
            result = get_book_author_utility()
            self.assertEqual(result, "VALID AUTHOR")

    @patch('builtins.input')
    def test_get_book_qty_utility_valid_input(self, mock_input):
        """Test get_book_qty_utility with valid input."""
        mock_input.return_value = "50"
        result = get_book_qty_utility()
        self.assertEqual(result, 50)

    @patch('builtins.input')
    def test_get_book_qty_utility_invalid_input(self, mock_input):
        """Test get_book_qty_utility with invalid input."""
        mock_input.side_effect = ["0", "-5", "25"]
        with patch('builtins.print'):
            result = get_book_qty_utility()
            self.assertEqual(result, 25)

    @patch('builtins.input')
    def test_get_update_field_utility_valid_inputs(self, mock_input):
        """Test get_update_field_utility with valid inputs."""
        valid_inputs = [
            "title", "author", "quantity", "TITLE", "Author", "QUANTITY"
        ]
        expected_outputs = [
            "title", "author", "quantity", "title", "author", "quantity"
        ]
        
        for input_val, expected_val in zip(valid_inputs, expected_outputs):
            mock_input.return_value = input_val
            result = get_update_field_utility()
            self.assertEqual(result, expected_val)

    @patch('builtins.input')
    def test_get_update_field_utility_invalid_input(self, mock_input):
        """Test get_update_field_utility with invalid input."""
        mock_input.side_effect = ["price", "category", "publisher"]
        with patch('builtins.print'):
            with self.assertRaises(ValueError) as context:
                get_update_field_utility()
            self.assertIn(
                "Aborting...you must enter 'Title', 'Author' or 'Quantity'", 
                str(context.exception)
            )

    @patch('builtins.input')
    def test_get_qty_action_utility_valid_inputs(self, mock_input):
        """Test get_qty_action_utility with valid inputs."""
        valid_inputs = ["add", "sub", "set", "ADD", "Sub", "SET"]
        expected_outputs = ["add", "sub", "set", "add", "sub", "set"]
        
        for input_val, expected_val in zip(valid_inputs, expected_outputs):
            mock_input.return_value = input_val
            result = get_qty_action_utility()
            self.assertEqual(result, expected_val)

    @patch('builtins.input')
    def test_get_qty_action_utility_invalid_input(self, mock_input):
        """Test get_qty_action_utility with invalid input."""
        mock_input.side_effect = ["increase", "decrease", "change"]
        with patch('builtins.print'):
            with self.assertRaises(ValueError) as context:
                get_qty_action_utility()
            self.assertIn(
                "Aborting...you must enter 'add' or 'sub' or 'set'", 
                str(context.exception)
            )

    @patch('functions.do_you_have_book_id_utility')
    @patch('functions.get_book_id_utility')
    def test_get_book_info_with_id(self, mock_get_id, mock_have_id):
        """Test get_book_info when user has book id."""
        mock_have_id.return_value = "yes"
        mock_get_id.return_value = 123
        
        result = get_book_info()
        self.assertEqual(result, {"id": 123})

    @patch('functions.do_you_have_book_id_utility')
    @patch('functions.get_book_title_utility')
    @patch('functions.get_book_author_utility')
    def test_get_book_info_without_id(
        self, mock_get_author, 
        mock_get_title, 
        mock_have_id
    ):
        """Test get_book_info when user doesn't have book id."""
        mock_have_id.return_value = "no"
        mock_get_title.return_value = "Test title"
        mock_get_author.return_value = "TEST AUTHOR"
        
        result = get_book_info()
        expected = {"title": "Test title", "author": "TEST AUTHOR"}
        self.assertEqual(result, expected)

    @patch('functions.get_book_title_utility')
    @patch('functions.get_book_author_utility')
    @patch('functions.get_book_qty_utility')
    def test_get_book(self, mock_get_qty, mock_get_author, mock_get_title):
        """Test get_book function."""
        mock_get_title.return_value = "Test title"
        mock_get_author.return_value = "TEST AUTHOR"
        mock_get_qty.return_value = 10
        
        result = get_book()
        self.assertIsInstance(result, Book)
        self.assertEqual(result.title, "Test title")
        self.assertEqual(result.author, "TEST AUTHOR")
        self.assertEqual(result.qty, 10)

    @patch('builtins.input')
    def test_get_book_search_query_valid_input(self, mock_input):
        """Test get_book_search_query with valid input."""
        mock_input.return_value = "search term"
        result = get_book_search_query()
        self.assertEqual(result, "search term")

    @patch('builtins.input')
    def test_get_book_search_query_with_extra_spaces(self, mock_input):
        """Test get_book_search_query with extra spaces."""
        mock_input.return_value = "search   term   with   spaces"
        result = get_book_search_query()
        self.assertEqual(result, "search term with spaces")

    @patch('builtins.input')
    def test_get_book_search_query_empty_input(self, mock_input):
        """Test get_book_search_query with empty input."""
        mock_input.side_effect = ["", "  ", "valid search"]
        with patch('builtins.print'):
            result = get_book_search_query()
            self.assertEqual(result, "valid search")

    def test_get_database_connection_params_valid_url(self):
        """Test get_database_connection_params with valid URL."""
        url = "mysql://user:password@localhost:3306/testdb"
        result = get_database_connection_params(url)
        expected = {
            'user': 'user',
            'password': 'password',
            'host': 'localhost',
            'port': '3306',
            'database': 'testdb'
        }
        self.assertEqual(result, expected)

    def test_get_database_connection_params_no_port(self):
        """Test get_database_connection_params without port."""
        url = "mysql://user:password@localhost/testdb"
        result = get_database_connection_params(url)
        expected = {
            'user': 'user',
            'password': 'password',
            'host': 'localhost',
            'database': 'testdb'
        }
        self.assertEqual(result, expected)

    def test_parse_cli_args_no_args(self):
        """Test parse_cli_args with no arguments."""
        with patch('sys.argv', ['ebookstore.py']):
            args = parse_cli_args()
            self.assertIsNone(args.connection_url)
            self.assertIsNone(args.database_file)
            self.assertIsNone(args.table_records)
            self.assertIsNone(args.table_name)

    def test_parse_cli_args_with_database_file(self):
        """Test parse_cli_args with database file argument."""
        with patch('sys.argv', ['ebookstore.py', '--database-file', 'test.db']):
            args = parse_cli_args()
            self.assertEqual(args.database_file, 'test.db')

    def test_parse_cli_args_with_connection_url(self):
        """Test parse_cli_args with connection URL argument."""
        with patch(
            'sys.argv', 
            ['ebookstore.py', '--connection-url', 'mysql://user:pass@host/db']
        ):
            args = parse_cli_args()
            self.assertEqual(args.connection_url, 'mysql://user:pass@host/db')

    def test_get_table_records_valid_file(self):
        """Test get_table_records with valid CSV file."""
        csv_content = (
            "id,title,author,qty\n"
            "1,Test Book,Test Author,10\n"
            "2,Another Book,Another Author,20"
        )
        
        with tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix='.csv'
        ) as temp_file:
            temp_file.write(csv_content)
            temp_file_path = temp_file.name
        
        try:
            table_records = []
            get_table_records(table_records, temp_file_path)
            
            expected = [
                ('1', 'Test Book', 'Test Author', '10'), 
                ('2', 'Another Book', 'Another Author', '20')
            ]
            self.assertEqual(table_records, expected)
        finally:
            os.unlink(temp_file_path)

    def test_get_table_records_file_not_found(self):
        """Test get_table_records with non-existent file."""
        table_records = []
        with self.assertRaises(SystemExit):
            get_table_records(table_records, "non_existent_file.csv")

    @patch('os.getenv')
    @patch('functions.load_dotenv')
    def test_get_database_connection_env_variable(
        self, mock_load_dotenv, mock_getenv
    ):
        """Test get_database_connection with environment variable."""
        mock_args = MagicMock()
        mock_args.database_file = None
        mock_args.connection_url = None
        mock_getenv.return_value = "mysql://user:pass@host/db"
        
        with patch(
            'functions.get_database_connection_params'
        ) as mock_get_params:
            mock_get_params.return_value = {'test': 'params'}
            params, db_file = get_database_connection(mock_args)
            
            self.assertEqual(params, {'test': 'params'})
            self.assertIsNone(db_file)

    @patch('os.getenv')
    @patch('functions.load_dotenv')
    def test_get_database_connection_no_connection(
        self, mock_load_dotenv, mock_getenv
    ):
        """Test get_database_connection with no connection provided."""
        mock_args = MagicMock()
        mock_args.database_file = None
        mock_args.connection_url = None
        mock_getenv.return_value = None
        
        with self.assertRaises(SystemExit):
            get_database_connection(mock_args)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_return_to_menu(self, mock_print, mock_input):
        """Test return_to_menu function."""
        mock_input.return_value = ""
        return_to_menu()
        mock_input.assert_called_once()

    @patch('builtins.print')
    @patch('builtins.exit')
    def test_exit_utility_sqlite(self, mock_exit, mock_print):
        """Test exit_utility with SQLite bookstore."""
        mock_bookstore = MagicMock(spec=BookStoreSqlite)
        mock_bookstore.db = MagicMock()
        mock_bookstore.cursor = MagicMock()
        
        exit_utility(mock_bookstore)
        
        mock_bookstore.cursor.close.assert_called_once()
        mock_bookstore.db.close.assert_called_once()
        mock_print.assert_called_with("\nGoodbye!!!")
        mock_exit.assert_called_once()

    @patch('builtins.print')
    @patch('builtins.exit')
    def test_exit_utility_mysql(self, mock_exit, mock_print):
        """Test exit_utility with MySQL bookstore."""
        # Create a mock that properly passes isinstance check
        mock_bookstore = MagicMock()
        mock_bookstore.__class__ = BookStoreMySQL
        mock_bookstore.db.is_connected.return_value = True
        mock_bookstore.cursor = MagicMock()
        
        exit_utility(mock_bookstore)
        
        mock_bookstore.cursor.close.assert_called_once()
        mock_bookstore.db.close.assert_called_once()
        mock_print.assert_called_with("\nGoodbye!!!")
        mock_exit.assert_called_once()

    @patch('builtins.print')
    @patch('builtins.exit')
    def test_exit_utility_mysql_not_connected(self, mock_exit, mock_print):
        """Test exit_utility with MySQL bookstore when not connected."""
        mock_bookstore = MagicMock()
        mock_bookstore.__class__ = BookStoreMySQL
        mock_bookstore.db.is_connected.return_value = False
        mock_bookstore.cursor = MagicMock()
        
        exit_utility(mock_bookstore)
        
        # When not connected, cursor and db close should not be called
        mock_bookstore.cursor.close.assert_not_called()
        mock_bookstore.db.close.assert_not_called()
        mock_print.assert_called_with("\nGoodbye!!!")
        mock_exit.assert_called_once()

    @patch('builtins.print')
    @patch('builtins.exit')
    def test_exit_utility_sqlite_no_db(self, mock_exit, mock_print):
        """Test exit_utility with SQLite bookstore when db is None."""
        mock_bookstore = MagicMock(spec=BookStoreSqlite)
        mock_bookstore.db = None
        mock_bookstore.cursor = MagicMock()
        
        exit_utility(mock_bookstore)
        
        # When db is None, cursor and db close should not be called
        mock_bookstore.cursor.close.assert_not_called()
        mock_print.assert_called_with("\nGoodbye!!!")
        mock_exit.assert_called_once()


class TestGetBookUpdateInfo(unittest.TestCase):
    """Test cases for get_book_update_info function."""

    @patch('functions.get_update_field_utility')
    @patch('functions.get_qty_action_utility')
    @patch('functions.get_book_qty_utility')
    def test_get_book_update_info_quantity(
        self, mock_get_qty, mock_get_action, mock_get_field
    ):
        """Test get_book_update_info for quantity field."""
        mock_get_field.return_value = "quantity"
        mock_get_action.return_value = "add"
        mock_get_qty.return_value = 5
        
        book_info = {"id": 1}
        result = get_book_update_info(book_info)
        
        expected = {
            "id": 1,
            "field": "quantity",
            "action": "add",
            "qty": 5
        }
        self.assertEqual(result, expected)

    @patch('functions.get_update_field_utility')
    @patch('functions.get_book_title_utility')
    def test_get_book_update_info_title(self, mock_get_title, mock_get_field):
        """Test get_book_update_info for title field."""
        mock_get_field.return_value = "title"
        mock_get_title.return_value = "New title"
        
        book_info = {"id": 1}
        result = get_book_update_info(book_info)
        
        expected = {
            "id": 1,
            "field": "title",
            "new_title": "New title"
        }
        self.assertEqual(result, expected)

    @patch('functions.get_update_field_utility')
    @patch('functions.get_book_author_utility')
    def test_get_book_update_info_author(self, mock_get_author, mock_get_field):
        """Test get_book_update_info for author field."""
        mock_get_field.return_value = "author"
        mock_get_author.return_value = "NEW AUTHOR"
        
        book_info = {"id": 1}
        result = get_book_update_info(book_info)
        
        expected = {
            "id": 1,
            "field": "author",
            "new_author": "NEW AUTHOR"
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
