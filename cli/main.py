import logging
import sys
from pathlib import Path
import os

# Set up the path to allow importing the library_manager package
# This is crucial when running the CLI file from the 'cli/' directory.
# It temporarily adds the parent directory (the project root) to the system path.
sys.path.append(os.path.abspath(os.path.join(Path(__file__).parent.parent)))

# Import the core classes from the library_manager package
try:
    from library_manager.inventory import LibraryInventory
    # Book is imported by LibraryInventory, but good practice to ensure it's available 
    # if needed directly, though not strictly required for the CLI logic here.
    # from library_manager.book import Book 
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import core library components. Make sure 'library_manager' folder and '__init__.py' exist. Error: {e}")
    sys.exit(1)


# --- Logging Setup (Task 5) ---
# Configure root logger for CLI interface
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    # Log output to console and a file
                    handlers=[
                        logging.StreamHandler(sys.stdout),
                        logging.FileHandler('library_cli.log')
                    ])
logger = logging.getLogger(__name__)


def get_validated_input(prompt, validator=lambda x: True, error_msg="Invalid input."):
    """
    Helper function for robust input validation (Task 4).
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                raise ValueError("Input cannot be empty.")
            if not validator(user_input):
                 raise ValueError(error_msg)
            return user_input
        except ValueError as e:
            print(f"ERROR: {e}")
            logger.error(f"Input validation failed for prompt '{prompt}': {e}")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None
        except EOFError:
            print("\nExiting input. Please try again.")
            logger.error("EOF received during input.")
            return None


def main_menu():
    """Displays the main menu options."""
    print("\n--- Library Inventory Manager ---")
    # Menu: Add Book, Issue Book, Return Book, View All, Search, Exit (Task 4)
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Catalog")
    print("6. Exit")
    
    # Validate the choice is a number between 1 and 6
    choice = get_validated_input(
        "Enter choice (1-6): ", 
        validator=lambda x: x.isdigit() and 1 <= int(x) <= 6, 
        error_msg="Choice must be between 1 and 6."
    )
    return choice


def main():
    """Main function to run the CLI application."""
    # Initialize the Inventory Manager; it attempts to load 'catalog.json'
    library = LibraryInventory()
    
    while True:
        # Task 5: try-except-finally blocks for user-facing loop
        try: 
            choice = main_menu()
            
            if choice is None: # Handled by get_validated_input on Ctrl+C/D
                continue

            if choice == '1': # Add Book
                print("\n--- Add New Book ---")
                title = get_validated_input("Enter Title: ")
                author = get_validated_input("Enter Author: ")
                # Simple ISBN validation: 10 or 13 digits
                isbn = get_validated_input(
                    "Enter ISBN (10 or 13 digits): ", 
                    validator=lambda x: (len(x) == 10 or len(x) == 13) and x.isdigit(), 
                    error_msg="ISBN must be 10 or 13 digits and contain only numbers."
                )
                
                if title and author and isbn:
                    if library.add_book(title, author, isbn):
                        print(f"SUCCESS: Book '{title}' added to the catalog.")
                    else:
                        print("FAILURE: Book could not be added (possible duplicate ISBN).")

            elif choice == '2': # Issue Book
                isbn = get_validated_input("Enter ISBN of book to Issue: ")
                if isbn:
                    book = library.search_by_isbn(isbn)
                    if book and book.issue():
                        print(f"SUCCESS: Book '{book.title}' has been issued.")
                    elif book:
                        print(f"FAILURE: Book '{book.title}' is already {book.status}.")
                    else:
                        print(f"ERROR: Book with ISBN {isbn} not found.")

            elif choice == '3': # Return Book
                isbn = get_validated_input("Enter ISBN of book to Return: ")
                if isbn:
                    book = library.search_by_isbn(isbn)
                    if book and book.return_book():
                        print(f"SUCCESS: Book '{book.title}' has been returned and is now available.")
                    elif book:
                        print(f"FAILURE: Book '{book.title}' was not issued.")
                    else:
                        print(f"ERROR: Book with ISBN {isbn} not found.")

            elif choice == '4': # View All Books
                print("\n--- All Books in Catalog ---")
                all_books = library.display_all()
                if all_books:
                    for i, book in enumerate(all_books, 1):
                        print(f"{i}. {book}")
                else:
                    print("The library catalog is currently empty.")

            elif choice == '5': # Search Catalog
                search_term = get_validated_input("Enter Title or ISBN to search: ")
                
                if search_term:
                    print("\n--- Search Results ---")
                    # Check for exact ISBN match first
                    book_by_isbn = library.search_by_isbn(search_term)
                    
                    if book_by_isbn:
                        print(f"[ISBN Match] {book_by_isbn}")
                    else:
                        # Search by title as a fallback
                        results = library.search_by_title(search_term)
                        if results:
                            print("\n[Title Matches]")
                            for book in results:
                                print(f"- {book}")
                        else:
                            print(f"No books found matching '{search_term}'.")

            elif choice == '6': # Exit
                print("Exiting Library Inventory Manager. Goodbye!")
                break
        
        except Exception as e:
            # Task 5: Catch all unexpected errors in the main loop
            logger.critical(f"A critical error occurred in the CLI loop: {e}", exc_info=True)
            print("\nA serious error occurred. Check 'library_cli.log' for details.")
        finally:
            # The 'finally' block can be used here to ensure cleanup or status reporting 
            # if necessary, but often left simple for a CLI main loop.
            pass


if __name__ == '__main__':
    main()