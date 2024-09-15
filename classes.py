# Import the following if they are not already imported:
try:
    import sqlite3 
    from sqlite3 import DatabaseError
    from sqlite3 import DataError
    from tabulate import tabulate
except ImportError:
    pass

class Book():
    '''A Book class to hold the book information...title, author, and 
    quantity in stock
    '''
    def __init__(self, title, author, qty):
        self.title = title
        self.author = author
        self.qty = qty


class BookStore():
    '''A BookStore class to manage the book store inventory. It takes
    the database file and an optional table as arguments'''
    def __init__(self, database_file, table=None):
        try:
            # Connect to sqlite
            self.db = sqlite3.connect(database_file)
            self.db.create_collation(  # Caseless comparison
                "UNICODE_NOCASE", BookStore.unicode_nocase_collation
            )
        except DatabaseError as e:
            self.db.rollback()  # Rollback any changes if error
            raise DatabaseError(
                "Error while setting up the database"
            ) from e
        except PermissionError as e:
            raise PermissionError(
                f"You don't have permission to create file '{database_file}'"
            ) from e
          
        try:    
            self.cursor = self.db.cursor()  # Get a cursor object

            # Create the table if it doesn't exist
            self.cursor.execute(
                '''CREATE TABLE IF NOT EXISTS book(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(255) COLLATE UNICODE_NOCASE NOT NULL,
                    author VARCHAR(255) COLLATE UNICODE_NOCASE NOT NULL,
                    qty INT NOT NULL,
                    CONSTRAINT book_table_key UNIQUE (title, author)
                );
                '''
            )
            self.db.commit()  # Changes were successful so commit
        except DatabaseError as e:
            self.db.rollback()  # Rollback any changes if error
            raise DatabaseError(
                "Error while creating a table in the database"
            ) from e

        try:
            # Insert table records into database if table is provided
            if table is not None:
                # If records exist in the database, replace them
                self.cursor.executemany(
                    '''INSERT OR IGNORE INTO book (id, title, author, qty) 
                    VALUES (?, ?, ?, ?)
                    ''', 
                    table
                )
                self.db.commit()  # Changes were successful so commit
        except DatabaseError as e:
            self.db.rollback()  # Rollback any changes if error
            raise DatabaseError(
                "Error while inserting to a table in the database"
            ) from e      


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


    def insert_book(self, book):
        '''Insert a book and it's details into the database. It takes a
        Book object as an argument. The Book object contains the book
        title, author, and quantity in stock. It prints out id of the
        book inserted. If the book already exists, it prints a message
        that the book already exists. If there is an error, it raises a
        DatabaseError'''
        try:
            self.cursor.execute(
                '''SELECT * FROM book 
                WHERE title = ? 
                AND author = ?
                ''', 
                (book.title, book.author)
            )
            if not self.cursor.fetchone():
                self.cursor.execute(
                    '''
                    INSERT INTO book (title, author, qty) 
                    VALUES (?, ?, ?)
                    ''', 
                    (book.title, book.author, book.qty)
                )
                self.db.commit()  # Changes were successful so commit
                print(f"\nBook entered with id: {self.cursor.lastrowid}")
            else:
                print("\nBook already exists")
        except DatabaseError as e:
            self.db.rollback()  # Rollback any changes if error
            raise DatabaseError(
                "Error while inserting a book to the database"
            ) from e 


    def update_book(self, book_info):
        '''Update a book in the database. It takes a dictionary as an
        argument. The dictionary contains the book id, title, author,
        quantity, and the field to update. If the book is found, it
        updates the book details and prints a message that the book was
        updated successfully. If the book is not found, it prints a
        message that the book was not found. If there is an error, it
        raises a DatabaseError
        '''
        try:
            book_found = False  # Inform user if book not found
            if "id" in book_info:  # If user provides the book id
                self.cursor.execute(
                    '''SELECT * FROM book 
                    WHERE id = ?
                    ''', 
                    (book_info["id"], )
                )
                record = self.cursor.fetchone()
                if record:  # If book exists
                    book_found = True
                    # If user wants to update quantity
                    if book_info["field"] == "quantity":
                        if book_info["action"] == "sub":
                            # Subtract from quantity
                            qty = record[3] - book_info["qty"]
                        elif book_info["action"] == "add":
                            # Add to quantity
                            qty = record[3] + book_info["qty"]  
                        else:  # Set quantity to a specific value
                            qty = book_info["qty"]  
                        if qty < 0:  # Book quantity can't be negative
                            raise DataError(
                                f"You can't perform this operation. You only \
have {record[3]} of this book in stock, but you want to reduce the stock by \
{book_info["qty"]} "
                            )
                        self.cursor.execute(
                            '''UPDATE book SET qty = ? 
                            WHERE id = ? 
                            ''', 
                            (
                                qty, 
                                book_info["id"]
                            )
                        )
                    # If user wants to update title
                    elif book_info["field"] == "title":
                        self.cursor.execute(
                            '''UPDATE book SET title = ? 
                            WHERE id = ?
                            ''', 
                            (book_info["new_title"], book_info["id"])
                        )
                    # If user wants to update author
                    else:
                        self.cursor.execute(
                            '''UPDATE book SET author = ? 
                            WHERE id = ?
                            ''', 
                            (book_info["new_author"], book_info["id"])
                        )
            # If user provides the book author and title        
            else:
                self.cursor.execute(
                    '''SELECT * FROM book 
                    WHERE author = ? 
                    AND title = ?
                    ''', 
                    (book_info["author"], book_info["title"])
                )
                record = self.cursor.fetchone()
                if record:  # If book exists
                    book_found = True
                    # If user wants to update quantity
                    if book_info["field"] == "quantity":
                        if book_info["action"] == "sub":
                            # Subtract from quantity
                            qty = record[3] - book_info["qty"]
                        elif book_info["action"] == "add":
                            # Add to quantity
                            qty = record[3] + book_info["qty"]  
                        else:  # Set quantity to a specific value
                            qty = book_info["qty"]  
                        if qty < 0:  # Book quantity can't be negative
                            raise DataError(
                                f"You can't perform this operation. You only \
have {record[3]} of this book in stock, but you want to reduce the stock by \
{book_info["qty"]}"
                            )
                        self.cursor.execute(
                            '''UPDATE book SET qty = ? 
                            WHERE author = ? 
                            AND title = ?
                            ''', 
                            (
                                qty, 
                                book_info["author"], 
                                book_info["title"]
                            )
                        )
                    # If user wants to update title
                    elif book_info["field"] == "title":
                        self.cursor.execute(
                            '''UPDATE book SET title = ? 
                            WHERE author = ? 
                            AND title = ?
                            ''', 
                            (
                                book_info["new_title"], 
                                book_info["author"], 
                                book_info["title"]
                            )
                        )
                    # If user wants to update author
                    else:
                        self.cursor.execute(
                            '''UPDATE book SET author = ? 
                            WHERE author = ? 
                            AND title = ?
                            ''', 
                            (
                                book_info["new_author"], 
                                book_info["author"], 
                                book_info["title"]
                            )
                        )
                    
            if book_found:
                self.db.commit()  # Changes were successful so commit
                print("\nBook updated successfully")
            else:
                print("\nBook not found")
        except DataError as e:
            self.db.rollback()
            raise DataError(
                f"You can't perform this operation. You only have {record[3]} \
of this book in stock, but you want to reduce the stock by {book_info["qty"]}"
            ) from e
        except DatabaseError as e:
            self.db.rollback()  # Rollback any changes if error
            raise DatabaseError(
                "Error while updating the book in the database"
            ) from e 

    def delete_book(self, book_info):
        '''Delete a book from the database. It takes a dictionary as 
        an argument. The dictionary contains the book id, title, and
        author. If the book is found, it deletes the book and prints a
        message that the book was deleted successfully. If the book is
        not found, it prints a message that the book was not found. If
        there is an error, it raises a DatabaseError.
        '''
        try:
            book_found = False  # Inform user if book not found
            if "id" in book_info:    # If user provides the book id
                self.cursor.execute(
                    '''SELECT * FROM book 
                    WHERE id = ?
                    ''', 
                    (book_info["id"], )
                )
                if self.cursor.fetchone():  # If book exists
                    book_found = True
                    self.cursor.execute(
                        '''DELETE FROM book 
                        WHERE id = ?
                        ''', 
                        (book_info["id"], )
                    )
            # If user provides the book author and title
            else:
                self.cursor.execute(
                    '''SELECT * FROM book 
                    WHERE author = ? 
                    AND title = ?
                    ''', 
                    (book_info["author"], book_info["title"])
                )
                if self.cursor.fetchone():  # If book exists
                    book_found = True
                    self.cursor.execute(
                        '''DELETE FROM book 
                        WHERE author = ? 
                        AND title = ?
                        ''', 
                        (book_info["author"], book_info["title"])
                    )
            if book_found:
                self.db.commit()  # Changes were successful so commit
                print("\nBook deleted successfully")
            else:
                print("\nBook not found")
        except DatabaseError as e:
            self.db.rollback()  # Rollback any changes if error
            raise DatabaseError(
                "Error while deleting the book in the database"
            ) from e  

                        
    def search_books(self, book_info):
        '''Search for a book in the database. It takes a dictionary as
        an argument. The dictionary contains the book id, title, and
        author. If the book is found, it prints the book details and 
        optionally that of other books that have a close match. If the 
        book is not found, it prints a message that the book was not 
        found. If there is an error, it raises a DatabaseError.
        '''
        try:
            if "title" in book_info and "author" in book_info:
                # Search for books if user knows the title and author
                self.cursor.execute(
                    '''SELECT * FROM book 
                    WHERE title = ? 
                    AND author = ?
                    ''', 
                    (book_info['title'], book_info['author'])
                )
            elif "id" in book_info:  # If user provides the book id
                self.cursor.execute(
                    '''SELECT * FROM book 
                    WHERE id = ?
                    ''', 
                    (book_info["id"], )
                )
            # If user provides the book author only
            elif "author" in book_info:
                self.cursor.execute(
                    '''SELECT * FROM book 
                    WHERE author = ?
                    ''', 
                    (book_info["author"], )
                )
            else:  # If user provides the book title only
                self.cursor.execute(
                    '''SELECT * FROM book 
                    WHERE title = ? 
                    ''', 
                    (book_info["title"], )
                )
            
            records = self.cursor.fetchall() # If book exists
            if not records:
                print("\nBook not found")
            else:  # Print the book details in a tabular format
                headers = ["ID", "Title", "Author", "Quantity"]
                print('\n', tabulate(records, headers))
        except DatabaseError as e:
            self.db.rollback()  # Rollback any changes if error
            raise DatabaseError(
                "Error while searching for the book in the database"
            ) from e
        except Exception as e:
            self.db.rollback()  # Rollback any changes if error
            raise Exception(
                "Sorry we can't proceed. You need to have the id or title or \
author or both of the book"
            ) from e
