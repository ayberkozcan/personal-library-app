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

        self.add_book_button = ctk.CTkButton(
            self,
            text="Add",
            command=self.add_book_page,
            fg_color="green"
        )

        self.add_book_button.grid(row=0, column=0, padx=10, pady=10)

    def add_book_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()
        
        header = ctk.CTkLabel(
            self,
            text="Add a Book",
            font=("Arial", 24, "bold")
        )
        header.grid(row=0, column=1, pady=20)

        for i, attr in enumerate(self.attributes):
            self.create_label_and_entry(attr, row=i+1)

        save_button = ctk.CTkButton(
            self,
            text="Save Book",
            command=self.save_book,
            fg_color="blue"
        )
        save_button.grid(row=len(self.attributes)+1, column=1, padx=10, pady=10)
        
        back_button = ctk.CTkButton(
            self,
            text="Back",
            command=self.homepage,
            fg_color="red"
        )
        back_button.grid(row=len(self.attributes)+2, column=1, padx=10, pady=10)

    def create_label_and_entry(self, text, row):
        label = ctk.CTkLabel(self, text=text)
        label.grid(row=row, column=0, padx=10, pady=10)

        entry = ctk.CTkEntry(self, placeholder_text="...",)
        entry.grid(row=row, column=1, padx=10, pady=10)

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