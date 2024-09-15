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
    get_book_search_info, exit_or_return, exit_utility

try:
    # Extract the database and table file paths from the command line 
    # arguments
    database_file = sys.argv[1]
    table_file = sys.argv[2]
#     if len(sys.argv) < 2:
#         print(
#             "Usage: python3 script_name.py database_file \
# [optional_table_records_file]"
#         )
#         sys.exit(1)

    # database_file = sys.argv[1]
    # table_file = sys.argv[2] if len(sys.argv) > 2 else None
   
    # Create the directory(s) if it/they doesn't exist
    try:
        os.makedirs(os.path.dirname(database_file), exist_ok=True)
    except PermissionError as e:
        raise PermissionError(
            f"You don't have permission to create directory \
    '{os.path.dirname(database_file)}'"
        ) from e

    # Create the directory(s) if it/they doesn't exist
    try:
        os.makedirs(os.path.dirname(table_file), exist_ok=True)
    except PermissionError as e:
        raise PermissionError(
            f"You don't have permission to create directory \
    '{os.path.dirname(table_file)}'"
        ) from e

    table = []  # Create an empty list to store the table records

    try:
        # Read the predefined records from a file into list table
        with open(table_file, 'r') as file:
            for index, line in enumerate(file):
                if index == 0:
                    continue
                record = line.strip().split('|')
                table.append((record[0], record[1], record[2], record[3]))
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"File '{table_file}' doesn't exist. Check your spelling"
        ) from e
    

    # Create an instance of the BookStore Database
    book_store = BookStore(database_file, table)

    while True:
        try:
            menu = input(
"""\nSelect one of the following options:
1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit
: """      
            ).strip()

            if menu == '1':
                
                try:
                    # Get the book details the first time from the user
                    book = get_book()
                    
                    # Insert the book details into the database
                    book_store.insert_book(book)
                    
                    # Ask the user if they want to exit or return to the
                    #  main menu
                    exit_or_return(book_store)
                except ValueError as e:
                    raise e
                except DatabaseError as e:
                    raise e

            if menu == '2':
                
                try:
                    # Get the book details from the user
                    book_info = get_book_info()
                    
                    # Get the book details for update from the user
                    book_update_info = get_book_update_info(book_info)
                    
                    # Update the book details in the database
                    book_store.update_book(book_update_info)

                    # Ask the user if they want to exit or return to the
                    #  main menu
                    exit_or_return(book_store)
                except ValueError as e:
                    raise e
                except DatabaseError as e:
                    raise e
            
            if menu == '3':
            
                try:
                    # Get the book details from the user
                    book_info = get_book_info()    

                    # Delete the book details from the database
                    book_store.delete_book(book_info)
                    
                    # Ask the user if they want to exit or return to the
                    #  main menu
                    exit_or_return(book_store)
                except ValueError as e:
                    raise e
                except DatabaseError as e:
                    raise e
                    
            if menu == '4':
                
                try:
                    # Get the book details from the user
                    # book_info = get_book_info()
                    book_info = get_book_search_info()  

                    # Search for the book details in the database
                    book_store.search_books(book_info)
                    
                    # Ask the user if they want to exit or return to the
                    #  main menu
                    exit_or_return(book_store)
                except ValueError as e:
                    raise e
                except DatabaseError as e:
                    raise e        

            if menu == '0':
                # Exit the application
                exit_utility(book_store) 
                    
        except ValueError as e:
            print('\n', e, sep='')
            exit_or_return(book_store)
        except DatabaseError as e:
            print('\n', e, sep='')
            exit_or_return(book_store)
        except Exception as e:
            print('\n', e, sep='')
            exit_or_return(book_store)

except FileNotFoundError as e:
    print(f'\nFile not found: {e}')
except PermissionError as e:
    print(f'\nPermission denied: {e}')
except DatabaseError as e:
    print(f'\nDatabase error: {e}')
    book_store.db.close()
