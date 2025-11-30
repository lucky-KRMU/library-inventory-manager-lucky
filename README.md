# 📚 Library Inventory Manager

**Course:** Programming for Problem Solving using Python
**Assignment Title:** Object-Oriented Design and Robust Programming in a Library Management System
**Author:** <Your Name Here>
**Submission Date:** 30th Nov, 2025

---

## 📌 Project Overview

This is a lightweight, command-line-based application designed to manage a campus library's book inventory. The system uses **Object-Oriented Programming (OOP)** principles to handle book records, track their status (issued/available), and maintain data persistence using a **JSON** file.

### Key Features

* **OOP Design (Task 1 & 2):** Implements **`Book`** and **`LibraryInventory`** classes with proper encapsulation and methods.
* **JSON Persistence (Task 3):** Automatically saves and loads the book catalog from the `catalog.json` file using the `json` module and `pathlib`.
* **Menu-Driven CLI (Task 4):** Provides an interactive interface for operations like Add Book, Issue Book, Return Book, View All, and Search.
* **Robust Exception Handling & Logging (Task 5):** Uses comprehensive `try-except-finally` blocks and the **`logging`** module to manage file errors and record key events (e.g., issuing/returning books).
* **Modular Structure (Task 6):** Organized as a Python package (`library_manager/`) separate from the interface (`cli/`).

---

## 🚀 How to Run the Application

### 1. Project Structure

The repository must be structured as follows:

.
├── A -  3
│   ├── README.md
│   ├── catalog.json
│   ├── cli
│   │   └── main.py
│   ├── library_manager
│   │   ├── __init__.py
│   │   ├── book.py
│   │   └── inventory.py
│   └── requirements.txt


### 2. Execution

1.  Navigate to the project's root directory in your terminal:
    ```bash
    cd library-inventory-manager-<yourname>
    ```
2.  Run the main interface file:
    ```bash
    python cli/main.py
    ```

### 3. Logging

Operational and error messages are recorded in two files in the root directory:
* **`library.log`**: For book-specific operations (e.g., issues, returns).
* **`library_cli.log`**: For main application events and critical errors in the CLI loop.

---

## 🛠️ Design Rationale

### Book Class (`book.py`)
* **Encapsulation:** All attributes (`title`, `author`, `isbn`, `status`) are managed through methods like `issue()` and `return_book()`.
* **JSON Integration:** The `to_dict()` method ensures the object can be easily serialized for persistence.

### LibraryInventory Class (`inventory.py`)
* **File I/O:** Private methods (`_load_books`, `_save_books`) handle file reading/writing using **`pathlib.Path`** for cross-OS compatibility.
* **Error Handling:** Catches `FileNotFoundError` and `json.JSONDecodeError` during loading to ensure the program can always start.

---

## ⚖️ Academic Integrity

This is an individual assignment. All code is original.

<I have taken help of internet for some modules specific work, such as geek for geeks, w3school, python.org and GenAI.>