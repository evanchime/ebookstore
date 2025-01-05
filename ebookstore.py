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

import argparse
import os
import sys
import csv
import logging  
from sqlite3 import DatabaseError as SQLiteDatabaseError
from mysql.connector.errors import DatabaseError as MySQLDatabaseError
from classes import BookStoreMySQL, BookStoreSqlite
from functions import(
    get_book, get_book_info, get_book_update_info,
    get_book_search_query, return_to_menu, exit_utility, 
    get_database_connection_params
)
from dotenv import load_dotenv

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description='Connect to a database and perform operations'
    )
    parser.add_argument(
        '--connection-url', type=str, help='MySQL connection URL'
    )
    parser.add_argument(
        '--database-file', type=str, help='Sqlite database file'
    )
    parser.add_argument(
        '--table-records', type=str, help='Predefined table records'
    )
    parser.add_argument(
        '--table-name', type=str, help='Table name. Defaults to book'
    )

    args = parser.parse_args()

    table_records = []

    if args.table_records:
        try:
            with open(args.table_records, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar="'")
                next(reader)
                for record in reader:
                    table_records.append(
                        (record[0], record[1], record[2], record[3])
                    )
        except FileNotFoundError:
            logging.error( 
                f"File not found: File {args.table_records} doesn't exist. " 
                "Check your spelling." )
            sys.exit(1)

    database_connection_params = None
    database_file = None

    if os.getenv("MYSQL_CONNECTION_URL"):
        database_connection_params = get_database_connection_params(
            os.getenv("MYSQL_CONNECTION_URL")
        )
    elif args.connection_url:
        database_connection_params = get_database_connection_params(
            args.connection_url
        )
    elif os.getenv("MYSQL_DATABASE_FILE"):
        database_file = os.getenv("MYSQL_DATABASE_FILE")
    elif args.database_file:
        database_file = args.database_file
    else:
        logging.error("No database connection provided. Exiting...")
        sys.exit(1)

    if database_connection_params:
        try:
            book_store = BookStoreMySQL(
                database_connection_params, args.table_name, table_records
            )
        except MySQLDatabaseError as e:
            logging.error(e)
            sys.exit(1)
    elif database_file:
        # Create the directory(s) if it/they doesn't exist
        try:
            if os.path.dirname(database_file): 
                os.makedirs(os.path.dirname(database_file), exist_ok=True)
            book_store = BookStoreSqlite(
                database_file, args.table_name, table_records
            )
        except PermissionError:
            logging.error(
                "Permission denied. You don't have permission to create "
                f"directory {os.path.dirname(database_file)}"
            )
            sys.exit(1)
        except SQLiteDatabaseError as e:
            logging.error(e)
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
                except SQLiteDatabaseError as e:
                    raise e
                except MySQLDatabaseError as e:
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
                except SQLiteDatabaseError as e:
                    raise e
                except MySQLDatabaseError as e:
                    raise e
                except Exception as e:
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
                except SQLiteDatabaseError as e:
                    raise e
                except MySQLDatabaseError as e:
                    raise e
            elif menu_1 == '4':
                try:
                    # Get the book details from the user
                    search_query = get_book_search_query()  

                    # Search for the book details in the database
                    book_store.search_books(search_query)
                    
                    # Return to main menu
                    return_to_menu()
                except ValueError as e:
                    raise e
                except SQLiteDatabaseError as e:
                    raise e
                except MySQLDatabaseError as e:
                    raise e        
            elif menu_1 == '0':
                # Exit the application
                exit_utility(book_store) 
            else:
                print("\nInvalid option. Please try again.")
        except ValueError as e:
            print('\n', e, sep='')
            return_to_menu()
        except SQLiteDatabaseError as e:
            print('\n', e, sep='')
            return_to_menu()
        except MySQLDatabaseError as e:
            print('\n', e, sep='')
            return_to_menu()
        except Exception as e:
            print('\n', e, sep='')
            return_to_menu()


if __name__ == "__main__":
    main()
