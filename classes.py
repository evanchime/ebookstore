# Import the following if they are not already imported:
try:
    import logging
    import sqlite3
    from sqlite3 import DatabaseError as SQLiteDatabaseError
    import mysql.connector
    from mysql.connector.errors import DatabaseError as MySQLDatabaseError
    from tabulate import tabulate
    from abstract_classes import BookStore
except ImportError as e:
    logging.error(f"Import error: {e}")
    raise ImportError("Failed to import necessary modules")


class Book:
    """A Book class to hold the book information...title, author, and 
    quantity in stock
    """
    def __init__(self, title, author, qty):
        self.title = title
        self.author = author
        self.qty = qty


class BookStoreSqlite(BookStore):
    """A BookStore class to manage the book store inventory. It takes
    the database file and an optional table as arguments
    """
    def __init__(
            self, database_connection, table_name='book', table_records=None
        ):
        try:
            self.table_name = table_name
            self._connect_to_db(database_connection)
            self._create_table()
            self._insert_predefined_records(table_records)
        except (SQLiteDatabaseError, PermissionError) as e:
            self._handle_db_error(e)
            

    def _connect_to_db(self, database_connection):
        """Connect to the database"""
        self.db = sqlite3.connect(database_connection)
        
        # Caseless comparison
        self.db.create_collation(  
            "UNICODE_NOCASE", BookStoreSqlite.unicode_nocase_collation
        )

        print(
            f"\nSuccessfully connected to SQLite " 
            f"database: {database_connection}"
        )


    def _create_table(self):
        """Create a table in the database"""
        self.cursor = self.db.cursor()

        self.cursor.execute(
            f'''CREATE TABLE IF NOT EXISTS {self.table_name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) COLLATE UNICODE_NOCASE NOT NULL,
                author VARCHAR(255) COLLATE UNICODE_NOCASE NOT NULL,
                qty INT NOT NULL,
                CONSTRAINT {self.table_name}_table_key 
                UNIQUE (title, author)
            );
            '''
        )
        self.db.commit()  


    def _insert_predefined_records(self, table_records):
        # Insert predefined table records into database if provided
        if table_records is not None:
            # If records exist in the database, don't throw an error
            self.cursor.executemany(
                f'''INSERT OR IGNORE INTO {self.table_name} 
                (id, title, author, qty) 
                VALUES (?, ?, ?, ?)
                ''', 
                table_records
            )
            self.db.commit()


    @staticmethod
    def unicode_nocase_collation(a: str, b: str):
        '''Custom collation. Function casefold ensures caseless unicode
        comparisons
        '''
        if a.casefold() == b.casefold():
            return 0
        if a.casefold() < b.casefold():
            return -1
        return 1
    

    def update_qty_utility(self, qty, book_info):
        '''Utility function to update the quantity of a book. It takes
        the updated quantity and a dictionary as arguments. The updated
        quantity is the quantity to update. The dictionary contains the
        book id, title, author, and the quantity to update. It updates
        the quantity of the book in the database
        '''
        if "id" in book_info:
            self.cursor.execute(
                f'''UPDATE {self.table_name} SET qty = ? 
                WHERE id = ? 
                ''', 
                (
                    qty, 
                    book_info["id"]
                )
            )
        else:
            self.cursor.execute(
                f'''UPDATE {self.table_name} SET qty = ? 
                WHERE author = ? 
                AND title = ?
                ''', 
                (
                    qty, 
                    book_info["author"], 
                    book_info["title"]
                )
            )


    def update_title_utility(self, book_info):
        '''Update the title of a book in the database.
         
        Args:
             book_info (dict): Contains book id, title, author, and 
             new title.
        '''
        if "id" in book_info:
            self.cursor.execute(
                f'''UPDATE {self.table_name} SET title = ? 
                WHERE id = ?
                ''', 
                (book_info["new_title"], book_info["id"])
            )
        else:
            self.cursor.execute(
                f'''UPDATE {self.table_name} SET title = ? 
                WHERE author = ? 
                AND title = ?
                ''', 
                (
                    book_info["new_title"], 
                    book_info["author"], 
                    book_info["title"]
                )
            )


    def update_author_utility(self, book_info):
        '''Update the author of a book in the database.
 
        Args:
             book_info (dict): Contains book id, title, author, and 
             new author.
        '''
        if "id" in book_info:
            self.cursor.execute(
                f'''UPDATE {self.table_name} SET author = ? 
                WHERE id = ?
                ''', 
                (book_info["new_author"], book_info["id"])
            )
        else:
            self.cursor.execute(
                f'''UPDATE {self.table_name} SET author = ? 
                WHERE author = ? 
                AND title = ?
                ''', 
                (
                    book_info["new_author"], 
                    book_info["author"], 
                    book_info["title"]
                )
            )


    def find_book(self, book_info):
        '''Find a book in the database using a dictionary containing
        the book id, title, and author. Returns the book details if 
        found, otherwise returns None.
        '''
        if "id" in book_info:
            self.cursor.execute(
                f'''SELECT * FROM {self.table_name} 
                WHERE id = ?
                ''', 
                (book_info["id"], )
            )
        else:
            self.cursor.execute(
                f'''SELECT * FROM {self.table_name} 
                WHERE author = ? 
                AND title = ?
                ''', 
                (book_info["author"], book_info["title"])
            )
        return self.cursor.fetchone()
    

    def insert_book(self, book):
        '''Insert a book into the database. If the book already exists, 
        it prints a message. If there is an error, it raises a 
        SQLiteDatabaseError.
        '''
        try:
            self.cursor.execute(
                f'''SELECT * FROM {self.table_name} 
                WHERE title = ? 
                AND author = ?
                ''', 
                (book.title, book.author)
            )
            if not self.cursor.fetchone():
                self.cursor.execute(
                    f'''
                    INSERT INTO {self.table_name} 
                    (title, author, qty) 
                    VALUES (?, ?, ?)
                    ''', 
                    (book.title, book.author, book.qty)
                )
                self.db.commit()
                print(f"\nBook entered with id: {self.cursor.lastrowid}")
            else:
                print("\nBook already exists")
        except SQLiteDatabaseError as e:
            self._handle_db_error(e)


    def delete_book(self, book_info):
        '''Delete a book from the database using a dictionary with the 
        book id, title, and author. Prints a success message if the book 
        is deleted, otherwise prints a not found message. Raises a 
        SQLiteDatabaseError on error.
        '''
        try:
            # Inform user if book not found
            book_found = False

            if "id" in book_info:  # If user provides the book id
                self.cursor.execute(
                    f'''SELECT * FROM {self.table_name} 
                    WHERE id = ?
                    ''', 
                    (book_info["id"], )
                )
                if self.cursor.fetchone():  # If book exists 
                    book_found = True
                    self.cursor.execute(
                        f'''DELETE FROM {self.table_name} 
                        WHERE id = ?
                        ''', 
                        (book_info["id"], )
                    )
            else:  # If user provides the book author and title
                self.cursor.execute(
                    f'''SELECT * FROM {self.table_name} 
                    WHERE author = ? 
                    AND title = ?
                    ''', 
                    (book_info["author"], book_info["title"])
                )
                if self.cursor.fetchone():  # If book exists
                    book_found = True
                    self.cursor.execute(
                        f'''DELETE FROM {self.table_name} 
                        WHERE author = ? 
                        AND title = ?
                        ''', 
                        (book_info["author"], book_info["title"])
                    )
            if book_found:
                self.db.commit()
                print("\nBook deleted successfully")
            else:
                print("\nBook not found")
        except SQLiteDatabaseError as e:
            self._handle_db_error(e)


    def search_books(self, search_query):
        '''Search for books in the database by id, title, or author. 
        Prints the book details if found, otherwise prints a not found 
        message. Raises a SQLiteDatabaseError on error.'''
        try:
            self.cursor.execute(
                f'''SELECT * FROM {self.table_name} 
                WHERE id LIKE ? 
                OR title LIKE ?
                OR author LIKE ?
                ''', 
                (
                    '%' + search_query + '%', 
                    '%' + search_query + '%', 
                    '%' + search_query + '%', 
                )
            )
            
            records = self.cursor.fetchall() 

            if not records:  # If book doesn't exist
                print("\nBook not found")
            else:  # Print the book details in a tabular format
                headers = ["ID", "Title", "Author", "Quantity"]
                print('\n', tabulate(records, headers))
        except SQLiteDatabaseError as e:
            self._handle_db_error(e)


class BookStoreMySQL(BookStore):
    '''A BookStore class to manage the book store inventory. It takes
    the database file and an optional table as arguments'''
    def __init__(
            self, database_connection, table_name='book', table_records=None
        ):
        try:
            self.table_name = table_name
            self._connect_to_db(database_connection)
            self._create_table()
            self._insert_predefined_records(table_records)
        except (MySQLDatabaseError, PermissionError) as e:
            self._handle_db_error(e)

        
    def _connect_to_db(self, database_connection):
        """Connect to the database"""
        self.db = mysql.connector.connect(
            host=database_connection["host"],
            database=database_connection["database"],
            user=database_connection["user"],
            password=database_connection["password"],
            port=(
                database_connection["port"] if "port" in database_connection 
                else 3306
            )
        )
        print(
            f"\nSuccessfully connected to MySQL " 
            f"database: {database_connection['database']}"
        )


    def _create_table(self):
        """Create a table in the database"""
        self.cursor = self.db.cursor()
        self.cursor.execute(
            f'''CREATE TABLE IF NOT EXISTS {self.table_name}(
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) 
                CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci 
                NOT NULL,
                author VARCHAR(255) 
                CHARACTER SET utf8mb4 
                COLLATE utf8mb4_unicode_ci 
                NOT NULL,
                qty INT NOT NULL,
                CONSTRAINT {self.table_name}_table_key 
                UNIQUE (title, author)
            );
            '''
        )
        self.db.commit()  


    def _insert_predefined_records(self, table_records):
        # Insert predefined table records into database if provided
        if table_records is not None:
            # If records exist in the database, don't throw an error
            self.cursor.executemany(
                f'''INSERT IGNORE INTO {self.table_name} 
                (id, title, author, qty) 
                VALUES (%s, %s, %s, %s)
                ''', 
                table_records
            )
            self.db.commit()


    def update_qty_utility(self, qty, book_info):
        '''Utility function to update the quantity of a book. It takes
        the updated quantity and a dictionary as arguments. The updated
        quantity is the quantity to update. The dictionary contains the
        book id, title, author, and the quantity to update. It updates
        the quantity of the book in the database
        '''
        if "id" in book_info:
            self.cursor.execute(
                f'''UPDATE {self.table_name} SET qty = %s 
                WHERE id = %s 
                ''', 
                (
                    qty, 
                    book_info["id"]
                )
            )
        else:
            self.cursor.execute(
                f'''UPDATE {self.table_name} SET qty = %s 
                WHERE author = %s 
                AND title = %s
                ''', 
                (
                    qty, 
                    book_info["author"], 
                    book_info["title"]
                )
            )


    def update_title_utility(self, book_info):
        '''Utility function to update the title of a book. It takes a
        dictionary as an argument. The dictionary contains the book id,
        title, author, and the new title. It updates the title of the
        book in the database
        '''
        if "id" in book_info:
            self.cursor.execute(
                f'''UPDATE {self.table_name} SET title = %s 
                WHERE id = %s
                ''', 
                (book_info["new_title"], book_info["id"])
            )
        else:
            self.cursor.execute(
                f'''UPDATE {self.table_name} SET title = %s 
                WHERE author = %s 
                AND title = %s
                ''', 
                (
                    book_info["new_title"], 
                    book_info["author"], 
                    book_info["title"]
                )
            )


    def update_author_utility(self, book_info):
        '''Utility function to update the author of a book. It takes a
        dictionary as an argument. The dictionary contains the book id,
        title, author, and the new author. It updates the author of the
        book in the database
        '''
        if "id" in book_info:
            self.cursor.execute(
                f'''UPDATE {self.table_name} SET author = %s 
                WHERE id = %s
                ''', 
                (book_info["new_author"], book_info["id"])
            )
        else:
            self.cursor.execute(
                f'''UPDATE {self.table_name} SET author = %s 
                WHERE author = %s 
                AND title = %s
                ''', 
                (
                    book_info["new_author"], 
                    book_info["author"], 
                    book_info["title"]
                )
            )


    def find_book(self, book_info):
        '''Find a book in the database. It takes a dictionary as an
        argument. The dictionary contains the book id, title, and
        author. If the book is found, it returns the book details. If
        the book is not found, it returns None. Book has to exist in
        order to be updated
        '''
        if "id" in book_info:
            self.cursor.execute(
                f'''SELECT * FROM {self.table_name} 
                WHERE id = %s
                ''', 
                (book_info["id"], )
            )
        else:
            self.cursor.execute(
                f'''SELECT * FROM {self.table_name} 
                WHERE author = %s 
                AND title = %s
                ''', 
                (book_info["author"], book_info["title"])
            )
        return self.cursor.fetchone()

    
    def insert_book(self, book):
        '''Insert a book and it's details into the database. It takes a
        Book object as an argument. The Book object contains the book
        title, author, and quantity in stock. It prints out id of the
        book inserted. If the book already exists, it prints a message
        that the book already exists. If there is an error, it raises a
        MySQLDatabaseError'''
        try:
            self.cursor.execute( 
                f'''SELECT * FROM {self.table_name} 
                WHERE title = %s 
                AND author = %s 
                ''', 
                (book.title, book.author) 
            ) 
            if not self.cursor.fetchone(): 
                self.cursor.execute( 
                    f'''INSERT INTO {self.table_name} (title, author, qty) 
                    VALUES (%s, %s, %s) 
                    ''', 
                    (book.title, book.author, book.qty) 
                ) 
                self.db.commit() 
                print(f"\nBook entered with id: {self.cursor.lastrowid}") 
            else: 
                print("\nBook already exists")
        except MySQLDatabaseError as e:
            self._handle_db_error(e) 


    def delete_book(self, book_info):
        '''Delete a book from the database. It takes a dictionary as 
        an argument. The dictionary contains the book id, title, and
        author. If the book is found, it deletes the book and prints a
        message that the book was deleted successfully. If the book is
        not found, it prints a message that the book was not found. If
        there is an error, it raises a MySQLDatabaseError.
        '''
        try:
            # Inform user if book not found 
            book_found = False 
            
            if "id" in book_info: # If user provides the book id 
                self.cursor.execute( 
                    f'''SELECT * FROM {self.table_name} 
                    WHERE id = %s 
                    ''', 
                    (book_info["id"], ) 
                ) 
                if self.cursor.fetchone(): # If book exists 
                    book_found = True 
                    self.cursor.execute( 
                        f'''DELETE FROM{self.table_name} 
                        WHERE id = %s 
                        ''', 
                        (book_info["id"], ) 
                    ) 
            else: # If user provides the book author and title 
                self.cursor.execute( 
                    f'''SELECT * FROM {self.table_name}
                    WHERE author = %s 
                    AND title = %s 
                    ''', 
                    (book_info["author"], book_info["title"]) 
                ) 
                if self.cursor.fetchone(): # If book exists 
                    book_found = True 
                    self.cursor.execute( 
                        f'''DELETE FROM {self.table_name}
                        WHERE author = %s 
                        AND title = %s 
                        ''', 
                        (book_info["author"], book_info["title"]) 
                    ) 
                if book_found: 
                    self.db.commit() 
                    print("\nBook deleted successfully") 
                else: 
                    print
                    ("\nBook not found")
        except MySQLDatabaseError as e:
            self._handle_db_error(e)  


    def search_books(self, search_query):
        '''Search the database against the user-provided input. If the 
        book is found, it prints the book details and optionally that of 
        other books that have a close match. If the book is not found, 
        it prints a message that the book was not found. If there is an 
        error, it raises a MySQLDatabaseError'''

        try:
            self.cursor.execute(
                f'''SELECT * FROM {self.table_name}
                WHERE id LIKE %s 
                OR title LIKE %s
                OR author LIKE %s
                ''', 
                (
                    '%' + search_query + '%', 
                    '%' + search_query + '%', 
                    '%' + search_query + '%', 
                )
            )

            records = self.cursor.fetchall()

            if not records:  # If book doesn't exist
                print("\nBook not found")
            else:  # Print the book details in a tabular format
                headers = ["ID", "Title", "Author", "Quantity"]
                print('\n', tabulate(records, headers))
        except MySQLDatabaseError as e:
            self._handle_db_error(e)
