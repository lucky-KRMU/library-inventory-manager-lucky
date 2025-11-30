import logging

# Configure logging for the book module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# A file handler to log book-specific events
file_handler = logging.FileHandler('library.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Book:
    """
    Represents a single book in the library catalog.
    """
    def __init__(self, title, author, isbn, status="available"):
        """
        Initializes a new Book object.
        Attributes: title, author, isbn, status ('available' or 'issued')
        """
        # Attributes: title, author, isbn, status
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status # 'available' or 'issued'

    def __str__(self):
        """
        Returns a user-friendly string representation of the Book object.
        """
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - Status: {self.status.capitalize()}"

    def to_dict(self):
        """
        Returns a dictionary representation of the book, useful for JSON serialization.
        """
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'status': self.status
        }

    def is_available(self):
        """
        Checks if the book is currently available.
        """
        return self.status == "available"

    def issue(self):
        """
        Changes the book status to 'issued' if available.
        """
        if self.is_available():
            self.status = "issued"
            logger.info(f"Book issued successfully: {self.title} ({self.isbn})") # Task 5: Logging
            return True
        else:
            logger.error(f"Attempted to issue unavailable book: {self.title} ({self.isbn}). Current status: {self.status}") # Task 5: Logging
            return False

    def return_book(self):
        """
        Changes the book status to 'available'.
        """
        if self.status == "issued":
            self.status = "available"
            logger.info(f"Book returned successfully: {self.title} ({self.isbn})") # Task 5: Logging
            return True
        else:
            logger.error(f"Attempted to return book that was not issued: {self.title} ({self.isbn}). Current status: {self.status}") # Task 5: Logging
            return False

if __name__ == '__main__':
    # Example usage for testing the Book class
    test_book = Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    print(test_book)
    print(test_book.to_dict())
    test_book.issue()
    test_book.issue() # Fails and logs error
    test_book.return_book()
    print(test_book)