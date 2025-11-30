import json
import logging
import sys
from pathlib import Path 

# Assuming the 'library_manager' package structure is set up, 
# we import Book using relative import.
# Note: This file will need a __init__.py in its parent directory 
# (library_manager/) and book.py must exist in the same directory.
try:
    from .book import Book
except ImportError:
    # Fallback for direct execution/testing if not run as part of a package
    sys.path.append(str(Path(__file__).parent.parent))
    from library_manager.book import Book


# --- Logging Setup (Task 5) ---
logger = logging.getLogger(__name__)
# Set a lower level for the logger in this module
logger.setLevel(logging.INFO)

# Create a handler to output logs to console (INFO level)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
# Define a professional formatter
formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class LibraryInventory:
    """
    Manages the collection of Book objects and handles file persistence 
    using JSON (Task 2 & 3).
    """
    def __init__(self, catalog_file='catalog.json'):
        """
        Initializes the inventory and attempts to load books from file.
        """
        # Task 3: Use pathlib.Path for file operations
        self.catalog_file = Path(catalog_file)
        self.books = []  # Task 2: Maintain a list of Book objects.
        self._load_books()

    def _load_books(self):
        """
        Loads the book catalog from the JSON file.
        Handles missing or corrupted files with try-except (Task 3 & 5).
        """
        # Task 5: Use try-except-finally for file operation
        try: 
            if not self.catalog_file.exists():
                raise FileNotFoundError
                
            with open(self.catalog_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Recreate Book objects from dictionaries
                self.books = [Book(**book_dict) for book_dict in data]
                logger.info(f"Successfully loaded {len(self.books)} books from {self.catalog_file}")
                
        except FileNotFoundError:
            logger.warning(f"Catalog file not found at {self.catalog_file}. Starting with an empty inventory.")
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON file: {self.catalog_file}. File may be corrupted.")
            # If corrupted, start with empty list to prevent runtime errors
            self.books = []
        except Exception as e:
            logger.error(f"An unexpected error occurred during loading: {e}", exc_info=True)
            self.books = []
        finally:
            # Task 5: finally block (ensures self.books is a list)
            if not isinstance(self.books, list):
                 self.books = []

    def _save_books(self):
        """
        Saves the current book catalog to the JSON file (Task 3).
        """
        # Task 5: Use try-except-finally
        try:
            # Convert Book objects to dictionaries for JSON serialization using to_dict()
            data = [book.to_dict() for book in self.books]
            
            # Ensure the parent directory exists if using subfolders
            self.catalog_file.parent.mkdir(parents=True, exist_ok=True) 

            with open(self.catalog_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
                logger.info(f"Successfully saved {len(self.books)} books to {self.catalog_file}")
        except Exception as e:
            logger.error(f"Error saving books to JSON file: {e}", exc_info=True)
        finally:
            pass # Simple finally block for completeness

    def add_book(self, title, author, isbn):
        """
        Adds a new Book object to the inventory (Task 2).
        """
        # Check for duplicate ISBN
        if any(book.isbn == isbn for book in self.books):
            logger.warning(f"Book with ISBN {isbn} already exists. Addition skipped.")
            return False

        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        self._save_books()
        return True

    def search_by_title(self, query):
        """
        Searches for books whose title contains the query string (case-insensitive) (Task 2).
        """
        query = query.lower()
        return [book for book in self.books if query in book.title.lower()]

    def search_by_isbn(self, query):
        """
        Searches for a book by its exact ISBN (Task 2).
        Returns the Book object or None if not found.
        """
        return next((book for book in self.books if book.isbn == query), None)

    def display_all(self):
        """
        Returns all books in the inventory (Task 2).
        """
        return self.books