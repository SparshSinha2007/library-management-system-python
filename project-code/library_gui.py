import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv
import os
from datetime import datetime

CSV_FILE = "books.csv"
FIELDNAMES = ["id", "title", "author", "status", "issued_to", "issue_date"]

def initialize_csv():
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

def load_books():
    books = []
    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append(row)
    return books

def save_books(books):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for b in books:
            writer.writerow(b)

def generate_book_id(books):
    if not books:
        return "1"
    ids = [int(b["id"]) for b in books if b["id"].isdigit()]
    return str(max(ids) + 1)

def add_book_gui():
    def add_book_action():
        title = entry_title.get().strip()
        author = entry_author.get().strip()
        if not title:
            messagebox.showerror("Error", "Title cannot be empty")
            return

        books = load_books()
        new_id = generate_book_id(books)

        new_book = {
            "id": new_id,
            "title": title,
            "author": author,
            "status": "Available",
            "issued_to": "",
            "issue_date": ""
        }

        books.append(new_book)
        save_books(books)
        messagebox.showinfo("Success", f"Book Added with ID: {new_id}")
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Add Book")
    add_window.geometry("300x200")

    tk.Label(add_window, text="Book Title:").pack()
    entry_title = tk.Entry(add_window)
    entry_title.pack()

    tk.Label(add_window, text="Author Name:").pack()
    entry_author = tk.Entry(add_window)
    entry_author.pack()

    tk.Button(add_window, text="Add Book", command=add_book_action).pack(pady=10)

def view_books_gui():
    books = load_books()

    view_window = tk.Toplevel(root)
    view_window.title("View All Books")
    view_window.geometry("700x300")

    tree = ttk.Treeview(view_window, columns=FIELDNAMES, show="headings")
    for col in FIELDNAMES:
        tree.heading(col, text=col.upper())
        tree.column(col, width=100)
    tree.pack(fill=tk.BOTH, expand=True)

    for b in books:
        tree.insert("", tk.END, values=list(b.values()))

def search_book_gui():
    term = simpledialog.askstring("Search", "Enter Book ID or Title:")
    if not term:
        return

    books = load_books()
    results = [b for b in books if term.lower() in b["title"].lower() or b["id"] == term]

    if not results:
        messagebox.showinfo("Result", "No matching book found.")
        return

    res_window = tk.Toplevel(root)
    res_window.title("Search Result")
    res_window.geometry("700x200")

    tree = ttk.Treeview(res_window, columns=FIELDNAMES, show="headings")
    for col in FIELDNAMES:
        tree.heading(col, text=col.upper())
        tree.column(col, width=100)
    tree.pack(fill=tk.BOTH, expand=True)

    for b in results:
        tree.insert("", tk.END, values=list(b.values()))

def issue_book_gui():
    book_id = simpledialog.askstring("Issue Book", "Enter Book ID:")
    if not book_id:
        return

    books = load_books()
    for b in books:
        if b["id"] == book_id:
            if b["status"] == "Issued":
                messagebox.showerror("Error", "Book already issued")
                return

            borrower = simpledialog.askstring("Borrower", "Enter Borrower Name:")
            if not borrower:
                return

            b["status"] = "Issued"
            b["issued_to"] = borrower
            b["issue_date"] = datetime.now().strftime("%Y-%m-%d")
            save_books(books)

            messagebox.showinfo("Success", "Book issued successfully")
            return

    messagebox.showerror("Error", "Book ID not found")

def return_book_gui():
    book_id = simpledialog.askstring("Return Book", "Enter Book ID:")
    if not book_id:
        return

    books = load_books()
    for b in books:
        if b["id"] == book_id:
            if b["status"] != "Issued":
                messagebox.showerror("Error", "Book is not issued")
                return

            b["status"] = "Available"
            b["issued_to"] = ""
            b["issue_date"] = ""
            save_books(books)

            messagebox.showinfo("Success", "Book returned successfully")
            return

    messagebox.showerror("Error", "Book ID not found")

def delete_book_gui():
    book_id = simpledialog.askstring("Delete Book", "Enter Book ID:")
    if not book_id:
        return

    books = load_books()
    new_books = [b for b in books if b["id"] != book_id]

    if len(new_books) == len(books):
        messagebox.showerror("Error", "Book ID not found")
        return

    save_books(new_books)
    messagebox.showinfo("Success", "Book deleted successfully")

# GUI Main Window
root = tk.Tk()
root.title("Library Management System")
root.geometry("400x450")
root.config(bg="#e0f7fa")

tk.Label(root, text="Library Management System", font=("Arial", 16, "bold"), bg="#e0f7fa").pack(pady=15)

tk.Button(root, text="Add Book", width=25, command=add_book_gui).pack(pady=5)
tk.Button(root, text="View All Books", width=25, command=view_books_gui).pack(pady=5)
tk.Button(root, text="Search Book", width=25, command=search_book_gui).pack(pady=5)
tk.Button(root, text="Issue Book", width=25, command=issue_book_gui).pack(pady=5)
tk.Button(root, text="Return Book", width=25, command=return_book_gui).pack(pady=5)
tk.Button(root, text="Delete Book", width=25, command=delete_book_gui).pack(pady=5)

tk.Button(root, text="Exit", width=25, bg="red", fg="white", command=root.quit).pack(pady=20)

initialize_csv()
root.mainloop()
