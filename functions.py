# Import the modules below, if not already imported
try:
    import re
    from classes import Book  # Book class from the classes.py file
except ImportError:
    pass

def get_book_id_utility():
    '''Get the id of the book from the user. The user provides the id
    of the book. The function returns the id of the book. The id of the
    book must be a whole number greater than zero.
    '''
    count = 0  # Reset

    book_id = input("\nEnter the id of the book: ").strip()

    # The book id should be a whole number greater than zero in no
    # more than 3 attempts
    while not re.fullmatch(r"[1-9][0-9]*", book_id):
        count += 1
        if count == 3:
            count = 0
            raise ValueError(
                "Aborting...book id must be whole number greater than 0"
            )
        print(
            "\nBook id must be whole number greater than zero. "
            "Please try again."      
        )
        book_id = input("\nEnter the id of the book: ").strip()

    # The database is expecting an integer
    return int(book_id)


def do_you_have_book_id_utility():
    '''Ask the user if they have the id of the book. The user provides
    'yes' or 'no'. The function returns 'yes' or 'no'. The user has 3
    attempts to provide the correct input of 'yes' or 'no'.
    '''
    count = 0  # The number of times user enters an invalid input

    ans = input(
        "\nDo you have the id of the book? 'yes' or 'no': "
    ).casefold().strip()

    # User has 3 attempts to provide correct input of 'yes' or 'no'
    while ans not in ["yes", "no"]:
        count += 1
        if count == 3:
            count = 0
            raise ValueError(
                "Aborting...you must enter 'yes' or 'no' if you have the id "
                "of the book"             
            )
        print(
            "\nPlease try again. Enter 'yes' or 'no' if you have the id of "
            "the book"
        )
        ans = input(
            "\nDo you have the id of the book? 'yes' or 'no': "
        ).casefold().strip()

    return ans


def get_book_title_utility(new_title=None):
    '''Get the title of the book from the user. The user provides the
    title of the book. The function returns the title of the book. The
    title of the book cannot be empty. The user has 3 attempts to
    provide the title of the book. The function takes an optional
    argument new_title. If new_title is provided, the function will
    prompt the user to enter the new title of the book.
    '''
    count = 0  # The number of times user enters an invalid input

    # If the field to update is title
    title_prompt = new_title if new_title else "title"

    title = input(f"\nEnter the {title_prompt} of the book: ").strip()

    # Title can not be empty after 3 attempts
    while not title:
        count += 1
        if count == 3:
            count = 0
            raise ValueError(f"Aborting...{title_prompt} cannot be empty.")
        print(
            f"\n{title_prompt.capitalize()} can't be empty. Please try again."
        )
        title = input(f"\nEnter the {title_prompt} of the book: ").strip()

    # Ensure no excess space in title user provided
    return re.sub(r" +", " ", title)


def get_book_author_utility(new_author=None):
    '''Get the author of the book from the user. The user provides the
    author of the book. The function returns the author of the book. The
    author of the book cannot be empty. The user has 3 attempts to
    provide the author of the book. The function takes an optional
    argument new_author. If new_author is provided, the function will
    prompt the user to enter the new author of the book.
    '''
    count = 0  # The number of times user enters an invalid input

    # If the field to update is author
    author_prompt = new_author if new_author else "author"

    author = input(f"\nEnter the {author_prompt} of the book: ").strip()

    # Author cannot be empty after 3 attempts
    while not author:
        count += 1
        if count == 3:
            count = 0
            raise ValueError(f"Aborting...{author_prompt} cannot be empty.")
        print(
            f"\n{author_prompt.capitalize()} can't be empty. Please try again."
        )
        author = input(f"\nEnter the {author_prompt} of the book: ").strip()

    # Ensure no excess space in author user provided
    return re.sub(r" +", " ", author)


def get_book_qty_utility():
    '''Get the quantity of the book from the user. The user provides the
    quantity of the book. The function returns the quantity of the book.
    The quantity of the book must be a whole number greater than zero.
    The user has 3 attempts to provide the quantity of the book.
    '''
    count = 0  # Reset

    qty = input("\nWhat quantity of the book: ").strip()

    # Quantity must be a whole number greater than zero after 3 attempts
    while not re.fullmatch(r"[1-9][0-9]*", qty):
        count += 1
        if count == 3:
            count = 0
            raise ValueError(
                "Aborting...quantity must be whole number greater than 0"
            )
        print(
            "\nQuantity must be whole number greater than zero. "
            "Please try again."      
        )
        qty = input("\nWhat quantity of the book: ").strip()

    # The database is expecting an integer
    return int(qty)


def get_update_field_utility():
    '''Get the field to update from the user. The user provides the
    field to update. The function returns the field to update. The field
    can be 'Title', 'Author' or 'Quantity'. The user has 3 attempts to
    provide the correct input of the field to update.
    '''
    count = 0  # The number of times user enters an invalid input

    field = input(
        "\nWhat field do you want to update? 'Title', 'Author' or 'Quantity': "
    ).casefold().strip()

    # User has 3 attempts to provide correct input of field to update
    while field not in [
    "title", "author", "quantity"
    ]:
        count += 1
        if count == 3:
            count = 0
            raise ValueError(
                "Aborting...you must enter 'Title', 'Author' or 'Quantity' to "
                "update"
            )
        print(
            "\nPlease try again. You must enter a valid field to update"
        )
        field = input(
            "\nWhat field do you want to update? "
            "'Title', 'Author' or 'Quantity': "
        ).casefold().strip()

    return field


def get_qty_action_utility():
    '''Get the action to perform on the quantity from the user. The user
    provides the action to perform on the quantity. The function returns
    the action to perform on the quantity. The action can be 'add',
    'sub' or 'set'. The user has 3 attempts to provide the correct input
    of the action to perform on the quantity.
    '''
    count = 0

    # User adds to, subtracts from  or sets the quantity of the book
    action = input(
        "\nDo you want to add to or subtract from the quantity or set to "
        "a new quantity? Enter 'add' or 'sub' or 'set': "
    ).casefold().strip()

    # User has 3 attempts to provide correct input of 'add' or 'sub'
    # or 'set' to update the quantity
    while action not in ["add", "sub", "set"]:
        count += 1
        if count == 3:
            count = 0
            raise ValueError(
                "Aborting...you must enter 'add' or 'sub' or 'set' "
                "to update the quantity"
            )
        print(
            "\nPlease try again. You must enter 'add' or 'sub' or 'set' "
            "to update the quantity"
        )
        action = input(
            "\nDo you want to add to or subtract from the quantity "
            "or set to a new quantity? Enter 'add' or 'sub' or 'set': "
        ).casefold().strip()

    return action


def get_book_info():
    '''Get book information from the user. The user can provide the id 
    of the book or the title and author of the book. If the user 
    provides the id of the book, the function will return the id of the 
    book in a dictionary. If the user provides the title and author of 
    the book, the function will return the title and author of the book,
    '''
    book_info = {}  # Dictionary to store and return book information
    
    ans = do_you_have_book_id_utility()

    if ans == "yes":
        book_info["id"] = get_book_id_utility() 
    else:
        book_info["title"] = get_book_title_utility()

        book_info["author"] = get_book_author_utility()

    return book_info


def get_book():
    '''Get book information from the user. The user provides the title, 
    author and quantity of the book. The function returns the book
    object created from the user inputs...title, author and quantity
    '''
    title = get_book_title_utility()
    
    author = get_book_author_utility()
    
    qty = get_book_qty_utility()

    return Book(title, author, qty)


def get_book_update_info(book_info):
    '''Get book information from the user. The user provides the field
    to update, the new value of the field and if quantity to update, the 
    action to perform on the quantity. The function returns the field, 
    the new value of the field and action on quantity stored in a 
    dictionary called book_info. The field can be 'Title', 'Author' or 
    'Quantity'. If the field is 'Quantity', the user can choose to add 
    to, subtract from or set the quantity of the book. 
    '''
    book_info["field"] = get_update_field_utility()

    if book_info["field"] == "quantity": 
        book_info["action"] = get_qty_action_utility()
                
        book_info["qty"] = get_book_qty_utility()
    elif book_info["field"] == "title":
        book_info["new_title"] = get_book_title_utility("new title")
    else:
        book_info["new_author"] = get_book_author_utility("new author")

    return book_info


def get_book_search_query():
    '''Get book search query from the user.'''
    count = 0  # The number of times user enters an invalid input

    search_query = input("\nEnter the search query: ").strip()
    
    # User has 3 attempts to provide correct input
    while not search_query:
        count += 1
        if count == 3:
            count = 0
            raise ValueError(
                "Aborting...you must enter a search query"
            )
        print(
            "\nPlease try again."
        )
        search_query = input("\nEnter the search query: ").strip()

    return re.sub(r" +", " ", search_query)


def exit_utility(book_store):
    '''Close the database connection. Print a goodbye message. Exit 
    the application. 
    '''
    book_store.db.close()
    print("\nGoodbye!!!")
    exit()


def return_to_menu ():
    '''Return to the main menu.'''
    input("\nPress enter to return to the main menu: ")
