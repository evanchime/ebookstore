try:
    import logging
    from sqlite3 import Error as SQliteError
    from mysql.connector.errors import Error as MySQLError
    from abc import ABC, abstractmethod
except ImportError as e:
    logging.error(f"Import error: {e}")
    raise ImportError("Failed to import necessary modules")

class BookStore(ABC):
    '''An abstract class to manage the book store inventory. It takes
    the database file and an optional table as arguments
    '''
    @abstractmethod
    def __init__(self, database_file, table_name='book', table_records=None):
        pass


    @abstractmethod 
    def _connect_to_db(self, database_file):
        pass

    @abstractmethod
    def _create_table(self):
        pass


    @abstractmethod
    def _insert_predefined_records(self, table_records):
        pass


    def _handle_db_error(self, e):
        """Handle errors"""
        self.db.rollback()
        line_no = e.__traceback__.tb_lineno
        file_name = e.__traceback__.tb_frame.f_code.co_filename
        if isinstance(e, SQliteError):
            raise Exception(
                f"Error on line {line_no} in '{file_name}': {str(e)}"
            ) from e
        elif isinstance(e, MySQLError):
            raise Exception(
                f"Error on line {line_no} in '{file_name}': {str(e)}"
            ) from e
        elif isinstance(e, PermissionError):
            raise PermissionError(
                f"Error on line {line_no} in '{file_name}': {str(e)}"
            ) from e
        else:
            raise Exception(
                f"Error on line {line_no} in '{file_name}': {str(e)}"
            ) from e


    @abstractmethod
    def update_qty_utility(self, qty, book_info):
        pass


    @abstractmethod
    def update_title_utility(self, book_info):
        pass


    @abstractmethod
    def update_author_utility(self, book_info):
        pass


    @abstractmethod
    def find_book(self, book_info):
        pass
 

    @abstractmethod
    def insert_book(self, book):
        pass


    @abstractmethod
    def delete_book(self, book_info):
        pass


    @abstractmethod
    def search_books(self, search_query):
        pass


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
            raise Exception(
                "You can't perform this operation. You only "
                f"have {record[3]} of this book in stock, "
                "but you want to reduce the stock by "
                f"{book_info["qty"]}"
            )
        return qty


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
        except SQliteError as e:
            self.db.rollback()
            # Get the line number and file name where the error occurred
            line_no = e.__traceback__.tb_lineno
            file_name = e.__traceback__.tb_frame.f_code.co_filename
            raise Exception(
                f"Error on line {line_no} in '{file_name}': {str(e)}"
            ) from e 
        except MySQLError as e:
            self.db.rollback()
            # Get the line number and file name where the error occurred
            line_no = e.__traceback__.tb_lineno
            file_name = e.__traceback__.tb_frame.f_code.co_filename
            raise Exception(
                f"Error on line {line_no} in '{file_name}': {str(e)}"
            ) from e
        except Exception as e:
            self.db.rollback()
            raise Exception(
                f"Error on line {line_no} in '{file_name}': {str(e)}"
            ) from e
