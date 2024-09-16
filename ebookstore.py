'''A program that can be used by a bookstore clerk. The program allows 
the clerk to:
- Add new books to the database
- Update book information
- Delete books from the database
- Search the database to find a specific book

The program takes two command line arguments:
- 1st argument is path to the database file named 'data/ebookstore_db'. 
Feel free to use another file
- 2nd argument is path to the file containing a predefined table records
named 'table_records.txt' note: the second argument is optional

The program will use the sqlite3 database to store the book records.

Also the program will be using classes and functions in seperate files 
to be imported.
'''

from sqlite3 import DatabaseError 
from tabulate import tabulate
import os
import sys
from classes import BookStore
from functions import get_book, get_book_info, get_book_update_info, \
    get_book_search_info, return_to_menu, exit_utility

if len(sys.argv) < 2:
    print(
        "An error occurred: Not enough arguments provided. " 
        "Usage: python3 script_name.py "
        "database_file [optional_table_records_file]"
    )
    sys.exit(1)
    
database_file = sys.argv[1]
table_records_file = sys.argv[2] if len(sys.argv) > 2 else None

# Create the directory(s) if it/they doesn't exist
try:
    os.makedirs(os.path.dirname(database_file), exist_ok=True)
except PermissionError:
    print(
        "Permission denied.You don't have permission to create directory "
        f"{os.path.dirname(database_file)}"
    )
    sys.exit(1)

# Create an empty list to store the table records
table_records = []  

if table_records_file:  # If predefined table records file is provided

    try:
        with open(table_records_file, 'r') as file:
            for index, line in enumerate(file):
                if index == 0:
                    continue
                record = line.strip().split('|')
                table_records.append(
                    (record[0], record[1], record[2], record[3])
                )
    except FileNotFoundError:
        print(
            f"File not found: File '{table_records_file}' doesn't exist. "
            "Check your spelling"
        )
        sys.exit(1)

try:
    book_store = BookStore(database_file, table_records)
except DatabaseError as e:
    print(f'Database error: {e}')
    sys.exit(1)
except PermissionError as e:
    print(f'Permission denied: {e}')
    sys.exit(1)

while True:
    try:
        menu_1 = input(
"""\nSelect one of the following options:
1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit
: """      
        ).strip()

        if menu_1 == '1':
            try:
                # Get the book details the first time from the user
                book = get_book()
                
                # Insert the book details into the database
                book_store.insert_book(book)
                
                # Return to the main menu
                return_to_menu()
            except ValueError as e:
                raise e
            except DatabaseError as e:
                raise e
        elif menu_1 == '2':
            try:
                # Get the book details from the user
                book_info = get_book_info()
                
                # Get the book details for update from the user
                book_update_info = get_book_update_info(book_info)
                
                # Update the book details in the database
                book_store.update_book(book_update_info)

                # Return to main menu
                return_to_menu()
            except ValueError as e:
                raise e
            except DatabaseError as e:
                raise e
        elif menu_1 == '3':
            try:
                # Get the book details from the user
                book_info = get_book_info()    

                # Delete the book details from the database
                book_store.delete_book(book_info)
                
                # Return to main menu
                return_to_menu()
            except ValueError as e:
                raise e
            except DatabaseError as e:
                raise e
        elif menu_1 == '4':
            try:
                # Get the book details from the user
                book_info = get_book_search_info()  

                # Search for the book details in the database
                book_store.search_books(book_info)
                
                # Return to main menu
                return_to_menu()
            except ValueError as e:
                raise e
            except DatabaseError as e:
                raise e        
        elif menu_1 == '0':
            # Exit the application
            exit_utility(book_store) 
        else:
            print("\nInvalid option. Please try again.")
    except ValueError as e:
        print('\n', e, sep='')
        return_to_menu()
    except DatabaseError as e:
        print('\n', e, sep='')
        return_to_menu()
