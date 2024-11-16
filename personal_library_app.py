import os
from tkinter import *
from tkinter import messagebox
import sqlite3
import customtkinter as ctk

class Library(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x800")
        self.title("My Library")

        ctk.set_default_color_theme("dark-blue")

        self.current_theme = "dark"
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.add_icon_path = os.path.join(BASE_DIR, "icons/add_icon.png")

        self.attributes = ["Book Name", "Author Name", "Publication Year", "Publisher", "Genre", "ISBN"]

        self.entries = {}

        self.connect_database()

        self.widgets()

    def connect_database(self):
        self.conn = sqlite3.connect("library.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_name TEXT,
                author_name TEXT,
                publication_year INTEGER,
                publisher TEXT,
                genre TEXT,
                isbn TEXT
            )
        """)
        self.conn.commit()

    def widgets(self):
        # Homepage
        self.homepage()

    def homepage(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        header = ctk.CTkLabel(
            self,
            text="Library",
            font=("Arial", 24, "bold")
        )
        header.grid(row=0, column=0, padx=20, pady=20)

        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()

        if not books:
            no_books_label = ctk.CTkLabel(self, text="No books...")
            no_books_label.grid(row=1, column=0, padx=20, pady=10)
        else:
            for i, book in enumerate(books, start=1):
                book_info = f"{book[1]} by {book[2]} ({book[3]})"
                book_label = ctk.CTkLabel(self, text=book_info)
                book_label.grid(row=i+1, column=0, padx=20, pady=5)

        add_icon = PhotoImage(file=self.add_icon_path)
        add_icon = add_icon.subsample(10, 10)

        self.add_book_button = ctk.CTkButton(
            self,
            image=add_icon,
            text="",
            command=self.add_book_page,
            height=35,
            width=35,
            fg_color="transparent",
            hover=None
        )

        self.add_book_button.grid(row=len(books)+2, column=0, padx=20, pady=10)

    def add_book_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=0, column=0, padx=20, pady=20)

        header = ctk.CTkLabel(
            center_frame,
            text="Add a Book",
            font=("Arial", 24, "bold")
        )
        header.grid(row=0, column=0, columnspan=2, pady=20)

        for i, attr in enumerate(self.attributes):
            self.create_label_and_entry_in_frame(center_frame, attr, row=i+1)

        save_button = ctk.CTkButton(
            center_frame,
            text="Save Book",
            command=self.save_book,
            fg_color="darkgreen"
        )
        save_button.grid(row=len(self.attributes)+1, column=0, columnspan=2, padx=10, pady=10)

        back_button = ctk.CTkButton(
            center_frame,
            text="Back",
            command=self.homepage,
            fg_color="darkred"
        )
        back_button.grid(row=len(self.attributes)+2, column=0, columnspan=2, padx=10, pady=10)

    def create_label_and_entry_in_frame(self, frame, text, row):
        label = ctk.CTkLabel(frame, text=text)
        label.grid(row=row, column=0, padx=10, pady=10, sticky="e")

        entry = ctk.CTkEntry(frame, placeholder_text="...")
        entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")

        self.entries[text] = entry

    def save_book(self):
        book_data = {key: entry.get() for key, entry in self.entries.items()}

        publication_year = book_data["Publication Year"]
        if not publication_year.isdigit():
            messagebox.showerror("Invalid Input", "Publication Year must be a valid Integer.")
            return
        
        isbn = book_data["ISBN"]
        if not isbn.isdigit():
            messagebox.showerror("Invalid Input", "ISBN must be a valid Integer.")
            return

        self.cursor.execute("""
            INSERT INTO books (book_name, author_name, publication_year, publisher, genre, isbn)
            VALUES (:book_name, :author_name, :publication_year, :publisher, :genre, :isbn)
        """, {
            "book_name": book_data["Book Name"],
            "author_name": book_data["Author Name"],
            "publication_year": book_data["Publication Year"],
            "publisher": book_data["Publisher"],
            "genre": book_data["Genre"],
            "isbn": book_data["ISBN"]
        })
        self.conn.commit()

        for entry in self.entries.values():
            entry.delete(0, END)

    def _del_(self):
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    app = Library()
    app.mainloop()