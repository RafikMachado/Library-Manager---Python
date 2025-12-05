# main.py
# Simple Library Manager (Python 3.9+)
# Run: python main.py

import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional

DATA_FILE = "library_data.json"

class Book:
    def __init__(self, title: str, author: str, genre: str, quantity: int):
        self.title = title
        self.author = author
        self.genre = genre
        self.quantity = quantity
        self.issued_count = 0  # times issued, for popularity

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "quantity": self.quantity,
            "issued_count": self.issued_count
        }

    @staticmethod
    def from_dict(d):
        b = Book(d["title"], d["author"], d["genre"], d["quantity"])
        b.issued_count = d.get("issued_count", 0)
        return b

class User:
    def __init__(self, name: str, contact: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.contact = contact
        self.borrowed = {}  # title -> due_date (ISO)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "contact": self.contact,
            "borrowed": self.borrowed
        }

    @staticmethod
    def from_dict(d):
        u = User(d["name"], d["contact"])
        u.id = d["id"]
        u.borrowed = d.get("borrowed", {})
        return u

class Transaction:
    def __init__(self, user_id: str, book_title: str, action: str, date: Optional[str]=None):
        self.user_id = user_id
        self.book_title = book_title
        self.action = action  # "issue" or "return"
        self.date = date or datetime.utcnow().isoformat()

    def to_dict(self):
        return {"user_id": self.user_id, "book_title": self.book_title, "action": self.action, "date": self.date}

    @staticmethod
    def from_dict(d):
        t = Transaction(d["user_id"], d["book_title"], d["action"], d.get("date"))
        return t

class Library:
    def __init__(self):
        self.books: Dict[str, Book] = {}  # title -> Book
        self.users: Dict[str, User] = {}  # id -> User
        self.transactions: List[Transaction] = []

    def add_book(self, title, author, genre, quantity):
        if title in self.books:
            self.books[title].quantity += quantity
        else:
            self.books[title] = Book(title, author, genre, quantity)

    def remove_book(self, title):
        if title in self.books:
            del self.books[title]
            return True
        return False

    def add_user(self, name, contact):
        u = User(name, contact)
        self.users[u.id] = u
        return u.id

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

    def issue_book(self, user_id, title):
        if user_id not in self.users:
            return False, "User not found"
        if title not in self.books:
            return False, "Book not found"
        book = self.books[title]
        if book.quantity <= 0:
            return False, "No copies available"
        user = self.users[user_id]
        # issue for 14 days
        due = (datetime.utcnow() + timedelta(days=14)).date().isoformat()
        user.borrowed[title] = due
        book.quantity -= 1
        book.issued_count += 1
        t = Transaction(user_id, title, "issue")
        self.transactions.append(t)
        return True, f"Issued. Due: {due}"

    def return_book(self, user_id, title):
        if user_id not in self.users:
            return False, "User not found"
        user = self.users[user_id]
        if title not in user.borrowed:
            return False, "User did not borrow this book"
        del user.borrowed[title]
        if title in self.books:
            self.books[title].quantity += 1
        else:
            # book was removed from catalog; re-add with 1 copy
            self.books[title] = Book(title, "Unknown", "Unknown", 1)
        t = Transaction(user_id, title, "return")
        self.transactions.append(t)
        return True, "Returned"

    def generate_report(self):
        report = {}
        report["total_books"] = sum(b.quantity for b in self.books.values())
        report["unique_titles"] = len(self.books)
        report["total_users"] = len(self.users)
        # popular books
        popular = sorted(self.books.values(), key=lambda b: b.issued_count, reverse=True)[:10]
        report["popular"] = [b.to_dict() for b in popular]
        # overdue users
        overdue = []
        today = datetime.utcnow().date()
        for u in self.users.values():
            for title, due in u.borrowed.items():
                try:
                    due_date = datetime.fromisoformat(due).date()
                except Exception:
                    due_date = datetime.strptime(due, "%Y-%m-%d").date()
                if due_date < today:
                    overdue.append({"user_id": u.id, "name": u.name, "book": title, "due": due})
        report["overdue"] = overdue
        return report

    def save_to_file(self, filename=DATA_FILE):
        data = {
            "books": {t: b.to_dict() for t, b in self.books.items()},
            "users": {uid: u.to_dict() for uid, u in self.users.items()},
            "transactions": [tr.to_dict() for tr in self.transactions]
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True

    def load_from_file(self, filename=DATA_FILE):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = {t: Book.from_dict(b) for t, b in data.get("books", {}).items()}
            self.users = {uid: User.from_dict(u) for uid, u in data.get("users", {}).items()}
            self.transactions = [Transaction.from_dict(t) for t in data.get("transactions", [])]
            return True
        except FileNotFoundError:
            return False

def prompt(s):
    return input(s).strip()

def main_menu():
    lib = Library()
    lib.load_from_file()
    while True:
        print("\nLibrary Manager")
        print("1 — Add book")
        print("2 — Remove book")
        print("3 — Add user")
        print("4 — Remove user")
        print("5 — Issue book")
        print("6 — Return book")
        print("7 — View books and users")
        print("8 — Save data")
        print("9 — Load data")
        print("0 — Exit")
        cmd = prompt("Select option: ")
        if cmd == "1":
            title = prompt("Title: ")
            author = prompt("Author: ")
            genre = prompt("Genre: ")
            qty = int(prompt("Quantity: "))
            lib.add_book(title, author, genre, qty)
            print("Book added.")
        elif cmd == "2":
            title = prompt("Title to remove: ")
            ok = lib.remove_book(title)
            print("Removed." if ok else "Not found.")
        elif cmd == "3":
            name = prompt("Name: ")
            contact = prompt("Contact info: ")
            uid = lib.add_user(name, contact)
            print("User added. ID:", uid)
        elif cmd == "4":
            uid = prompt("User ID to remove: ")
            ok = lib.remove_user(uid)
            print("Removed." if ok else "Not found.")
        elif cmd == "5":
            uid = prompt("User ID: ")
            title = prompt("Book title: ")
            ok, msg = lib.issue_book(uid, title)
            print(msg)
        elif cmd == "6":
            uid = prompt("User ID: ")
            title = prompt("Book title: ")
            ok, msg = lib.return_book(uid, title)
            print(msg)
        elif cmd == "7":
            print("Books:")
            for b in lib.books.values():
                print(f" - {b.title} by {b.author} [{b.quantity} copies] (issued {b.issued_count} times)")
            print("Users:")
            for u in lib.users.values():
                print(f" - {u.id} {u.name} borrowed: {u.borrowed}")
        elif cmd == "8":
            lib.save_to_file()
            print("Saved.")
        elif cmd == "9":
            ok = lib.load_from_file()
            print("Loaded." if ok else "No data file.")
        elif cmd == "0":
            print("Goodbye.")
            break
        else:
            print("Unknown option.")

if __name__ == "__main__":
    main_menu()
