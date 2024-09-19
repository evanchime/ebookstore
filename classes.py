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
    def __init__(self, database_file, table_records=None):
        try:
            self.db = sqlite3.connect(database_file)
            # Caseless comparison
            self.db.create_collation(  
                "UNICODE_NOCASE", BookStore.unicode_nocase_collation
            )
        except DatabaseError as e:
            self.db.rollback() 
            self.db.close()
            # Get the line number and file name where the error occurred
            line_no = e.__traceback__.tb_lineno
            file_name = e.__traceback__.tb_frame.f_code.co_filename
            raise DatabaseError(
                f"Error on line {line_no} in '{file_name}' while setting up "
                "the database"
            ) from e
        except PermissionError as e:
            # Get the line number and file name where the error occurred
            line_no = e.__traceback__.tb_lineno
            file_name = e.__traceback__.tb_frame.f_code.co_filename
            raise PermissionError(
                f"Error on line {line_no} in file '{file_name}'. You don't "
                f"have permission to create file '{database_file}'"
            ) from e
          
        try:    
            self.cursor = self.db.cursor()

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
            self.db.commit()  
        except DatabaseError as e:
            self.db.rollback()
            # Get the line number and file name where the error occurred
            line_no = e.__traceback__.tb_lineno
            file_name = e.__traceback__.tb_frame.f_code.co_filename
            raise DatabaseError(
                f"Error on line {line_no} in file '{file_name}' while "
                "creating a table in the database"
            ) from e

        try:
            # Insert predefined table records into database if provided
            if table_records is not None:
                # If records exist in the database, don't throw an error
                self.cursor.executemany(
                    '''INSERT OR IGNORE INTO book (id, title, author, qty) 
                    VALUES (?, ?, ?, ?)
                    ''', 
                    table_records
                )
                self.db.commit()
        except DatabaseError as e:
            self.db.rollback()
            # Get the line number and file name where the error occurred
            line_no = e.__traceback__.tb_lineno
            file_name = e.__traceback__.tb_frame.f_code.co_filename
            raise DatabaseError(
                f"Error on line {line_no} in file '{file_name}' while "
                "inserting to a table in the database"
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
    

    @staticmethod
    def get_update_qty_utility(book_info, record):
        '''Utility function to get the updated quantity of a book. It
        takes a dictionary and a tuple as arguments. The dictionary
        contains the action to perform on the quantity and the quantity
        to update. The tuple contains the book details. It returns the
        updated quantity. If the quantity is negative, it raises a
        DataError
        '''
        if book_info["action"] == "sub":
            # Subtract from database quantity
            qty = record[3] - book_info["qty"]
        elif book_info["action"] == "add":
            # Add to database quantity
            qty = record[3] + book_info["qty"]  
        else:  # Set database quantity to a specific value
            qty = book_info["qty"]  
        if qty < 0:  # Book quantity can't be negative
            raise DataError(
                "You can't perform this operation. You only "
                f"have {record[3]} of this book in stock, "
                "but you want to reduce the stock by "
                f"{book_info["qty"]}"
            )
        return qty


    def update_qty_utility(self, qty, book_info):
        '''Utility function to update the quantity of a book. It takes
        the updated quantity and a dictionary as arguments. The updated
        quantity is the quantity to update. The dictionary contains the
        book id, title, author, and the quantity to update. It updates
        the quantity of the book in the database
        '''
        if "id" in book_info:
            self.cursor.execute(
                '''UPDATE book SET qty = ? 
                WHERE id = ? 
                ''', 
                (
                    qty, 
                    book_info["id"]
                )
            )
        else:
            self.cursor.execute('''UPDATE book SET qty = ? 
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
        '''Utility function to update the title of a book. It takes a
        dictionary as an argument. The dictionary contains the book id,
        title, author, and the new title. It updates the title of the
        book in the database
        '''
        if "id" in book_info:
            self.cursor.execute(
                '''UPDATE book SET title = ? 
                WHERE id = ?
                ''', 
                (book_info["new_title"], book_info["id"])
            )
        else:
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


    def update_author_utility(self, book_info):
        '''Utility function to update the author of a book. It takes a
        dictionary as an argument. The dictionary contains the book id,
        title, author, and the new author. It updates the author of the
        book in the database
        '''
        if "id" in book_info:
            self.cursor.execute(
                '''UPDATE book SET author = ? 
                WHERE id = ?
                ''', 
                (book_info["new_author"], book_info["id"])
            )
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


    def find_book(self, book_info):
        '''Find a book in the database. It takes a dictionary as an
        argument. The dictionary contains the book id, title, and
        author. If the book is found, it returns the book details. If
        the book is not found, it returns None. Book has to exist in
        order to be updated
        '''
        if "id" in book_info:
            self.cursor.execute(
                '''SELECT * FROM book 
                WHERE id = ?
                ''', 
                (book_info["id"], )
            )
        else:
            self.cursor.execute(
                '''SELECT * FROM book 
                WHERE author = ? 
                AND title = ?
                ''', 
                (book_info["author"], book_info["title"])
            )
        return self.cursor.fetchone()
    

    def update_books_utilty(self, book_info, record):
        '''Utility function to update the book details. It takes a
        dictionary and a tuple as arguments. The dictionary contains the
        book id, title, author, the field to update and the new value.
        The tuple contains the book details. It updates the book details
        in the database
        '''
        # If user wants to update quantity
        if book_info["field"] == "quantity":
            qty = self.get_update_qty_utility(book_info, record)
            self.update_qty_utility(qty, book_info)
        # If user wants to update title
        elif book_info["field"] == "title":
            self.update_title_utility(book_info)
        else: # If user wants to update author
            self.update_author_utility(book_info)


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
                self.db.commit()
                print(f"\nBook entered with id: {self.cursor.lastrowid}")
            else:
                print("\nBook already exists")
        except DatabaseError as e:
            self.db.rollback()
            # Get the line number and file name where the error occurred
            line_no = e.__traceback__.tb_lineno
            file_name = e.__traceback__.tb_frame.f_code.co_filename
            raise DatabaseError(
                f"Error on line {line_no} on file '{file_name}' while "
                "inserting a book to the database"
            ) from e 


    def update_book(self, book_info):
        '''Update a book in the database. It takes a dictionary as an
        argument. The dictionary contains the book id, title, author,
        the field to update and the new value, and if quantity to 
        update, the action on the quantity. If the book is found, it
        updates the book details and prints a message that the book was
        updated successfully. If the book is not found, it prints a
        message that the book was not found. If there is an error, it
        raises a DatabaseError
        '''
        try:
            if "id" in book_info:  # If user provides the book id
                record = self.find_book(book_info) 
                if record:  # If book exists 
                    self.update_books_utilty(book_info, record)       
            else:  # If user provides the book author and title 
                record = self.find_book(book_info)
                if record:  # If book exists
                    self.update_books_utilty(book_info, record)
                    
            if record:
                self.db.commit()
                print("\nBook updated successfully")
            else:
                print("\nBook not found")
        except DataError as e:
            self.db.rollback()
            # Get the line number and file name where the error occurred
            line_no = e.__traceback__.tb_lineno
            file_name = e.__traceback__.tb_frame.f_code.co_filename
            raise DataError(
                f"Error on line {line_no} in file '{file_name}'. You can't "
                f"perform this operation. You only have {record[3]} "
                "of this book in stock, but you want to reduce the stock by "
                f"{book_info["qty"]}"
            ) from e
        except DatabaseError as e:
            self.db.rollback()
            # Get the line number and file name where the error occurred
            line_no = e.__traceback__.tb_lineno
            file_name = e.__traceback__.tb_frame.f_code.co_filename
            raise DatabaseError(
                f"Error on line {line_no} in file '{file_name}' while "
                "updating the book in the database"
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
            # Inform user if book not found
            book_found = False

            if "id" in book_info:  # If user provides the book id
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
            else:  # If user provides the book author and title
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
                self.db.commit()
                print("\nBook deleted successfully")
            else:
                print("\nBook not found")
        except DatabaseError as e:
            self.db.rollback()
            # Get the line number and file name where the error occurred
            line_no = e.__traceback__.tb_lineno
            file_name = e.__traceback__.tb_frame.f_code.co_filename
            raise DatabaseError(
                f"Error on line {line_no} in file '{file_name}' while "
                "deleting the book in the database"
            ) from e  


    def search_books(self, search_query):
        '''Search the database against the user-provided input. If the 
        book is found, it prints the book details and optionally that of 
        other books that have a close match. If the book is not found, 
        it prints a message that the book was not found. If there is an 
        error, it raises a DatabaseError'''
        try:
            self.cursor.execute(
                '''SELECT * FROM book 
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
        except DatabaseError as e:
            self.db.rollback()
            # Get the line number and file name where the error occurred
            line_no = e.__traceback__.tb_lineno
            file_name = e.__traceback__.tb_frame.f_code.co_filename
            raise DatabaseError(
                f"Error on line {line_no} in file '{file_name}' while "
                "searching for the book in the database"
            ) from e
