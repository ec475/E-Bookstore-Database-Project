import sqlite3

############################ SET UP DATABASE ############################

# Connect to database and set cursor.
db = sqlite3.connect('ebookstore')
cursor = db.cursor()

# Create table. 
cursor.execute('''
               CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY,  Title VARCHAR(15), Author VARCHAR(15), Qty INTEGER)
''')
db.commit()

# Add values for rows in table.
rows = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30), 
        (3002, 'Harry Potter and the Philosophers Stone', 'J.K. Rowling', 40),
        (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
        (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37),
        (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]

# Insert rows into the table.
cursor.executemany('''INSERT OR IGNORE INTO books(id, Title, Author, Qty) VALUES(?, ?, ?, ?)''', rows)
db.commit()

############################ SET UP FUNCTIONS ############################

def enter_book():
    '''
    Function to add a book to the table
    '''
    # Set new id. 
    id = cursor.execute('''SELECT MAX(id) FROM books''')
    newid = cursor.fetchone()[0] + 1
    # Ask for input of title and author. 
    title = input("What is the title of the book you would like to enter?")
    author = input(f"Who is the author of {title}?")
    # Ask for input of quantity. 
    while True:
        copies = input(f"How many copies of {title} are in the bookstore?")
        # Add book to table if quantity is a number.
        try:
            int(copies)
            cursor.execute('''INSERT INTO books(id, Title, Author, Qty) VALUES(?, ?, ?, ?)''', (newid, title, author, copies))
            db.commit()
            print(f"{title} has been entered into the database.")
            break
        # Otherwise prompt for numerical quantity.
        except ValueError:
            print("Please ensure quantity entered is a number.")
            continue

def update_book():
    '''
    Function to update a book in the table.
    '''
    cursor.execute('''SELECT id, Title FROM books''')
    # Print books so user can choose ID. 
    for row in cursor:
        print('{0} : {1}'.format(row[0], row[1]))
    while True:
        # Ask which book to edit. 
        id = input("Please enter the id of the book you would like to update: ")
        cursor.execute('''SELECT id FROM books WHERE id = ?''', (id,))
        # If the book is in the table, ask user what they want to edit and get input. 
        if cursor.fetchone():
            while True:
                to_edit = input("Which would you like to edit (1,2,3):\n\
                    1. Title\n\
                    2. Author\n\
                    3. Qty\n")
                # Edit title if user selects this.
                if to_edit == '1':
                    title = input("Please enter the new title: ")
                    cursor.execute('''UPDATE books SET Title = ? WHERE id = ?''', (title, id))
                    db.commit()
                    print("Your book has been successfully updated.\n")
                    break
                # Edit author if user selects this.
                elif to_edit == '2':
                    author = input("Please enter the new author: ")
                    cursor.execute('''UPDATE books SET Author = ? WHERE id = ?''', (author, id))
                    db.commit()
                    print("Your book has been successfully updated.\n")
                    break
                # Edit quantity if user selects this. 
                elif to_edit == '3':
                    while True:
                        qty = input(f"How many copies are in the bookstore?")
                        try:
                            int(qty)
                            cursor.execute('''UPDATE books SET Qty = ? WHERE id = ?''', (qty, id))
                            db.commit()
                            print("Your book has been successfully updated.\n")
                            break
                        except ValueError:
                            print("Please ensure quantity entered is a number.\n")
                            continue
                    break
                else:
                    print("Please enter a valid choice (1-3).")
                    continue
            break
        else:
            print("Please enter a valid id.")
            continue

def delete_book():
    '''
    Function to delete book.
    '''
    while True:
        cursor.execute('''SELECT id, Title FROM books''')
        # Print ids and titles.
        for row in cursor:
            print('{0} : {1}'.format(row[0], row[1]))
        # Get input of book to delete.
        id = input("\nPlease enter the id of the book you would like to delete: ")
        cursor.execute('''SELECT id FROM books WHERE id = ?''', (id,))
        result = cursor.fetchone()
        # If a book exists with that id, delete it. 
        if result:
            cursor.execute('''DELETE FROM books WHERE id = ?''', (id,))
            db.commit()
            print("Your book has been successfully deleted.\n")
            break
        # Otherwise ask for a valid id. 
        else: 
            print("\nPlease enter a valid id.\n")
            continue


def search_title():
    '''
    Function to search for a book by title
    '''
    while True:
        # Get input for which book to search.
        title = input("Please enter the title you would like to search for or press 0 to exit: ")
        if title == '0':
            break
        # Search for the book selected.
        else:
            cursor.execute('''SELECT * FROM books WHERE Title = ?''', (title,))
            # If there is a book with that id, print the book.
            if cursor.fetchone():
                cursor.execute('''SELECT * FROM books WHERE Title = ?''', (title,))
                for row in cursor:
                    print('\nid : {0}\nTitle: {1}\nAuthor: {2}\nQty: {3}\n\n'.format(row[0], row[1], row[2], row[3]))
                break
            # Otherwise, tell user that this book doesn't exist.
            else:
                print(f"There is no book with the title {title} in the database.\n")
                continue

def search_author():
    '''
    Function to search books by author
    '''
    while True:
        # Ask which author to search for. 
        author = input("Please enter the author you would like to search for or enter 0 to exit: ")
        if author == '0':
            break
        # Show books with this author if they exist, or print error message.
        else:
            cursor.execute('''SELECT * FROM books WHERE Author = ?''', (author,))
            if cursor.fetchone():
                cursor.execute('''SELECT * FROM books WHERE Author = ?''', (author,))
                for row in cursor:
                    print('\nid : {0}\nTitle: {1}\nAuthor: {2}\nQty: {3}\n\n'.format(row[0], row[1], row[2], row[3]))
                break
            else:
                print(f"There is no book with the author {author} in the database.\n")
                continue    

def search_books(): 
    '''
    Function to search books. 
    '''
    while True:
        # Ask whether to search by title or author and apply appropriate function.
        search_by = input("Which would you like to search by (1,2):\n\
            1. Title\n\
            2. Author\n")
        if search_by == '1':
            search_title()
            break
        elif search_by == '2':
            search_author()
            break
        else:
            print("Please enter a valid option.\n")
            continue


############################ MAIN PROGRAM ############################

# Ask user to input what they want to do. 
while True:
    choice = input("Make a choice from 1-4, or select 0 to exit:\n\
        1. Enter book\n\
        2. Update book\n\
        3. Delete book\n\
        4. Search books\n\
        0. Exit\n")
    # Enter book if user selects this.
    if choice == '1':
        enter_book()
        continue
    # Update book if user selects this.
    elif choice == '2':
        update_book()
        continue
    # Delete book if user selects this. 
    elif choice == '3':
        delete_book()
    # Search books if user selects this. 
    elif choice == '4':
        search_books()
    # Exit program if user selects this. 
    elif choice == '0':
        break
    # Otherwise, prompt for a valid selection.
    else:
        print("Please enter a valid option (0-4).")
        continue
