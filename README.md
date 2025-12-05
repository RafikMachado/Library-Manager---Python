

# **📙 README — Python Project: Library Manager**

## **Project Title**

**Library Manager**

## **Project Description**

Library Manager is an object-oriented Python application for managing books, users, borrowing, and returns.
It showcases OOP design principles, class interactions, JSON data storage, and a simple console interface.

The system supports book management, user registration, issuing and returning books, and generating library reports.

---

## **Features**

### 📚 Book Management

* Add, remove, update books
* Track quantity and genres

### 👤 User Management

* Add/remove users
* Store contact info and borrowed books

### 🔄 Borrowing System

* Issue books with quantity validation
* Return books
* Track borrowing history

### 📊 Reports

* Available vs borrowed books
* Most popular books
* Users with overdue returns

### 💾 Data Persistence

* Save data to JSON
* Load data at startup

---

## **Requirements**

* **Python 3.9+**
* No external dependencies required (uses built-in `json` module)

---

## **Running the Program**

```bash
python main.py
```

---

## **Project Structure**

```
/library_manager
   ├── main.py
   ├── book.py
   ├── user.py
   ├── library.py
   ├── transaction.py
   ├── data.json
   └── README.md
```

---

## **Main Classes**

### `Book`

* title, author, genre, quantity

### `User`

* name, contact info, borrowed books

### `Library`

* manages books, users, transactions
* methods include:

  * `add_book()`
  * `remove_book()`
  * `issue_book()`
  * `return_book()`
  * `generate_report()`
  * `save_to_file()`
  * `load_from_file()`

---

## **Main Menu**

```
1 — Add book
2 — Remove book
3 — Add user
4 — Remove user
5 — Issue book
6 — Return book
7 — View books and users
8 — Save data
9 — Load data
0 — Exit
```

---

## **Example Output**

```
Book issued successfully!
User: John Smith
Book: '1984' by George Orwell
Remaining copies: 2
```

---

## **Optional Enhancements**

* Due-date tracking
* Fines for overdue books
* Export reports to CSV or PDF
* GUI using Tkinter or PyQt

---

If you'd like, I can also **generate the full project code** for C, Haskell, or Python.
