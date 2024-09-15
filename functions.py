# Import the modules below, if not already imported
try:
    import re
    from classes import Book  # Book class from the classes.py file
except ImportError:
    pass

def get_book_info():
    '''Get book information from the user. The user can provide the id 
    of the book or the title and author of the book. If the user 
    provides the id of the book, the function will return the id of the 
    book in a dictionary. If the user provides the title and author of 
    the book, the function will return the title and author of the book,
    '''
    count = 0  # The number of times user enters an invalid input

    book_info = {}  # Dictionary to store and return book information

    ans = input(
        "\nDo you have the id of the book? 'yes' or 'no': "
    ).casefold().strip()

    # User has 3 attempts to provide correct input of 'yes' or 'no'
    while ans not in ["yes", "no"]:
        count += 1
        if count == 3:
            count = 0
            raise ValueError(
                "Aborting...you must enter 'yes' or 'no' if you have the \
id of the book"             
            )
        print(
            "\nPlease try again. Enter 'yes' or 'no' if you \
have the id of the book"
        )
        ans = input(
            "\nDo you have the id of the book? 'yes' or 'no': "
        ).casefold().strip()

    if ans == "yes":
        count = 0  # Reset

        book_info["id"] = input("\nEnter the id of the book: ").strip()

        # The book id should be a whole number greater than zero in no
        # more than 3 attempts
        while not re.fullmatch(r"[1-9][0-9]*", book_info["id"]):
            count += 1
            if count == 3:
                count = 0
                raise ValueError(
                    "Aborting...book id must be whole number greater than 0"
                )
            print(
                "\nBook id must be whole number greater than zero. \
Please try again."      
)
            book_info["id"] = input("\nEnter the id of the book: ").strip()

        # The database is expecting an integer
        book_info["id"] = int(book_info["id"])  
    else:
        count = 0  # Reset

        book_info["title"] = input(
            "\nEnter the title of the book: "
        ).strip().casefold()

        # The title can not be empty after 3 attempts
        while not book_info["title"]:
            count += 1
            if count == 3:
                count = 0
                raise ValueError("Aborting...title cannot be empty")
            print("\nTitle cannot be empty. Please try again.")
            book_info["title"] = input(
                "\nEnter the title of the book: "
            ).strip().casefold()

        book_info["title"] = re.sub(  # Ensure no excess space in title
            r" +", " ", book_info["title"]
        )

        count = 0

        book_info["author"] = input(
            "\nEnter the author of the book: "
        ).strip().casefold()

        # Author cannot be empty after 3 attempts
        while not book_info["author"]:
            count += 1
            if count == 3:
                count = 0
                raise ValueError("Aborting...author cannot be empty")
            print("\nAuthor cannot be empty. Please try again.")
            book_info["author"] = input(
                "\nEnter the author of the book: "
            ).strip().casefold()

         # Ensure no excess space in author
        book_info["author"] = re.sub( 
            r" +", " ", book_info["author"]
        )

    return book_info


def get_book():
    '''Get book information from the user. The user provides the title, 
    author and quantity of the book. The function returns the book
    object created from the user inputs...title, author and quantity
    '''
    count = 0  # The number of times user enters an invalid input
    user_input_title = input(
        "\nEnter the title of the book: "
    ).strip().casefold()

    # Title can not be empty after 3 attempts
    while not user_input_title:
        count += 1
        if count == 3:
            count = 0
            raise ValueError("Aborting...title cannot be empty.")
        print("\nTitle can't be empty. Please try again.")
        user_input_title = input(
            "\nEnter the title of the book: "
        ).strip().casefold()

    # Ensure no excess space in title user provided
    user_input_title = re.sub(r" +", " ", user_input_title)
    
    count = 0  # Reset
    user_input_author = input(
        "\nEnter the author of the book: "
    ).strip().casefold()

    # Author cannot be empty after 3 attempts
    while not user_input_author:
        count += 1
        if count == 3:
            count = 0
            raise ValueError("Aborting...author cannot be empty.")
        print("\nAuthor can't be empty. Please try again.")
        user_input_author = input(
            "\nEnter the author of the book: "
        ).strip().casefold()

    # Ensure no excess space in author user provided
    user_input_author = re.sub(r" +", " ", user_input_author)
    
    count = 0  # Reset

    user_input_qty = input(
        "\nEnter the quantiy of the book: "
    ).strip()

    # Quantity must be a whole number greater than zero after 3 attempts
    while not re.fullmatch(r"[1-9][0-9]*", user_input_qty):
        count += 1
        if count == 3:
            count = 0
            raise ValueError(
                "Aborting...quantity must be whole number greater than 0"
            )
        print(
            "\nQuantity must be whole number greater than zero. \
Please try again."      
        )
        user_input_qty = input(
            "\nEnter the quantiy of the book: "
        ).strip()

    # Create and return a book object from the user inputs. The database
    # is expecting an integer quantity
    return Book(user_input_title, user_input_author, int(user_input_qty))


def get_book_update_info(book_info):
    '''Get book information from the user. The user provides the field
    to update, the new value of the field and if quantity to update, the 
    action to perform on the quantity. The function returns the field, 
    the new value of the field and action on quantity stored in a 
    dictionary called book_info. The field can be 'Title', 'Author' or 
    'Quantity'. If the field is 'Quantity', the user can choose to add 
    to, subtract from or set the quantity of the book. 
    '''
    count = 0  # The number of times user enters an invalid input

    book_info["field"] = input(
        "\nWhat field do you want to update? 'Title', 'Author' or \
'Quantity': "
    ).casefold().strip()

    # User has 3 attempts to provide correct input of field to update
    while book_info["field"] not in [
    "title", "author", "quantity"
    ]:
        count += 1
        if count == 3:
            count = 0
            raise ValueError(
                "Aborting...you must enter 'Title', 'Author' or 'Quantity' to \
update"
            )
        print(
            "\nPlease try again. You must enter a valid field to update"
        )
        book_info["field"] = input(
            "\nWhat field do you want to update? 'Title', 'Author' or \
'Quantity': "
        ).casefold().strip()


    if book_info["field"] == "quantity": 
        count = 0

        # User adds to, subtracts from  or sets the quantity of the book
        book_info["action"] = input(
            "\nDo you want to add to or subtract from the quantity or set to \
a new quantity? Enter 'add' or 'sub' or 'set': "
        ).casefold().strip()

        # User has 3 attempts to provide correct input of 'add' or 'sub'
        # or 'set' to update the quantity
        while book_info["action"] not in ["add", "sub", "set"]:
            count += 1
            if count == 3:
                count = 0
                raise ValueError(
                    "Aborting...you must enter 'add' or 'sub' or 'set' to \
update the quantity"
                )
            print(
                "\nPlease try again. You must enter 'add' or 'sub' or 'set' \
to update the quantity"
            )
            book_info["action"] = input(
                "\nDo you want to add to or subtract from the quantity or set \
to a new quantity? Enter 'add' or 'sub' or 'set': "
            ).casefold().strip()
                
        count = 0  # Reset

        book_info["qty"] = input(
            "\nEnter the quantiy of the book: "
        )

        # User should enter quantity to update as a whole number greater
        # than zero in no more 3 input attempts
        while not re.fullmatch(r"[1-9][0-9]*", book_info["qty"]):
            count += 1
            if count == 3:
                count = 0
                raise ValueError(
                    "Aborting...quantity must be whole number greater than 0"
                )
            print(
                "\nQuantity must be whole number greater than zero. Please \
try again."      
            )
            book_info["qty"] = input(
                "\nEnter the quantiy of the book: "
            ).strip()
        book_info["qty"] = int(book_info["qty"])
    elif book_info["field"] == "title":
        count = 0  # Reset
        
        book_info["new_title"] = input(
            "\nEnter the new title of the book: "
        ).strip().casefold()

        # New title cannot be empty after 3 attempts
        while not book_info["new_title"]:
            count += 1
            if count == 3:
                count = 0
                raise ValueError(
                    "Aborting...new title cannot be empty"
                )
            print(
                "\nNew title cannot be empty. Please try again."
            )
            book_info["new_title"] = input(
                "\nEnter the new title of the book: "
            ).strip().casefold()

        # Ensure no excess space in new title
        book_info["new_title"] = re.sub(
            r" +", " ", book_info["new_title"]
        )
    else:
        count = 0  # Reset
        
        book_info["new_author"] = input(
            "\nEnter the new author of the book: "
        ).strip().casefold()

        # New author cannot be empty after 3 attempts
        while not book_info["new_author"]:
            count += 1
            if count == 3:
                count = 0
                raise ValueError(
                    "Aborting...new author cannot be empty"
                )
            print(
                "\nNew author cannot be empty. Please try again."
            )
            book_info["new_author"] = input(
                "\nEnter the new author of the book: "
            ).strip().casefold()

        # Ensure no excess space in new author
        book_info["new_author"] = re.sub(
            r" +", " ", book_info["new_author"]
        )

    return book_info


def get_book_search_info():
    '''Get book information from the user. The user can provide the id 
    of the book or the title or the author or both title and author of 
    the book. If the user provides the id of the book, or the title or 
    the author or both the function will return the values respectively 
    in a dictionary.
    '''
    count = 0  # The number of times user enters an invalid input

    book_info = {}  # Dictionary to store and return book information

    menu_2 = input('''\nDo you have:
1. The id
2. The title
3. The author name
4. The title and author name
5. None of the above
: ''').casefold().strip()
    
    # User has 3 attempts to provide correct input
    while menu_2 not in ['1', '2', '3', '4', '5']:
        count += 1
        if count == 3:
            count = 0
            raise ValueError(
                "Aborting...you must say if you have the id or title or \
author or both of the book"             
            )
        print(
            "\nPlease try again."
        )
        menu_2 = input('''\nDo you have:
1. The id
2. The title
3. The author name
4. The title and author name
5. None of the above
: ''').casefold().strip()
    
    if menu_2 == '1':
        count = 0

        book_info["id"] = input("\nEnter the id of the book: ").strip()

        # The book id should be a whole number greater than zero in no
        # more than 3 attempts
        while not re.fullmatch(r"[1-9][0-9]*", book_info["id"]):
            count += 1
            if count == 3:
                count = 0
                raise ValueError(
                    "Aborting...book id must be whole number greater than 0"
                )
            print(
                "\nBook id must be whole number greater than zero. \
Please try again."      
)
            book_info["id"] = input("\nEnter the id of the book: ").strip()

        # The database is expecting an integer
        book_info["id"] = int(book_info["id"]) 
    elif menu_2 == '2':
        count = 0

        book_info["title"] = input(
            "\nEnter the title of the book: "
        ).strip().casefold()

        # The title can not be empty after 3 attempts
        while not book_info["title"]:
            count += 1
            if count == 3:
                count = 0
                raise ValueError("Aborting...title cannot be empty")
            print("\nTitle cannot be empty. Please try again.")
            book_info["title"] = input(
                "\nEnter the title of the book: "
            ).strip().casefold()

        book_info["title"] = re.sub(  # Ensure no excess space in title
            r" +", " ", book_info["title"]
        )
    elif menu_2 == '3':
        count = 0 

        book_info["author"] = input(
            "\nEnter the author of the book: "
        ).strip().casefold()

        # Author cannot be empty after 3 attempts
        while not book_info["author"]:
            count += 1
            if count == 3:
                count = 0
                raise ValueError("Aborting...author cannot be empty")
            print("\nAuthor cannot be empty. Please try again.")
            book_info["author"] = input(
                "\nEnter the author of the book: "
            ).strip().casefold()

         # Ensure no excess space in author
        book_info["author"] = re.sub(
            r" +", " ", book_info["author"]
        )
    elif menu_2 == '4':
        count = 0

        book_info["title"] = input(
            "\nEnter the title of the book: "
        ).strip().casefold()

        # The title can not be empty after 3 attempts
        while not book_info["title"]:
            count += 1
            if count == 3:
                count = 0
                raise ValueError("Aborting...title cannot be empty")
            print("\nTitle cannot be empty. Please try again.")
            book_info["title"] = input(
                "\nEnter the title of the book: "
            ).strip().casefold()

        book_info["title"] = re.sub(  # Ensure no excess space in title
            r" +", " ", book_info["title"]
        )

        count = 0

        book_info["author"] = input(
            "\nEnter the author of the book: "
        ).strip().casefold()

        # Author cannot be empty after 3 attempts
        while not book_info["author"]:
            count += 1
            if count == 3:
                count = 0
                raise ValueError("Aborting...author cannot be empty")
            print("\nAuthor cannot be empty. Please try again.")
            book_info["author"] = input(
                "\nEnter the author of the book: "
            ).strip().casefold()

         # Ensure no excess space in author
        book_info["author"] = re.sub(
            r" +", " ", book_info["author"]
        )
    else:
        raise Exception(
            "Sorry we can't proceed. You need to have the id or title \
or author or both of the book"
        )  

    return book_info


def exit_or_return(book_store):
    '''Exit the application or return to the main menu. The user can 
    press enter to return to the main menu or 'x' to exit the 
    application
    '''
    user_input = input(
        "\nPress enter to return to the main menu or 'x' to exit: "
    ).casefold().strip()
    if user_input == 'x':
        exit_utility(book_store)


def exit_utility(book_store):
    '''Close the database connection. Print a goodbye message. Exit 
    the application. 
    '''
    book_store.db.close()
    print("\nGoodbye!!!")
    exit()
