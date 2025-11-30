# library_manager/__init__.py

"""
Initializes the library_manager package.
We use this file to make the main classes directly importable 
from the package namespace (e.g., from library_manager import Book, LibraryInventory).
"""

# Explicitly import the main classes from their respective modules
from .book import Book
from .inventory import LibraryInventory

# Define the __all__ variable to specify which objects are exposed 
# when 'from library_manager import *' is used.
__all__ = [
    'Book', 
    'LibraryInventory',
]

# You could optionally set up package-level logging here if needed, 
# but per-module logging (as done in book.py and inventory.py) is often clearer.