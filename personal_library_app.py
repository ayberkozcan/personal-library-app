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
        self.theme_icon_path = os.path.join(BASE_DIR, "icons/theme_icon.png")
        self.add_icon_path = os.path.join(BASE_DIR, "icons/add_icon.png")
        self.delete_icon_path = os.path.join(BASE_DIR, "icons/delete_icon.png")

        self.attributes = ["Name", "Author", "Publication Year", "Publisher", "Genre", "ISBN", "Page Count", "Pages Read", "Status"]

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
                isbn TEXT,
                page_count INTEGER,
                pages_read INTEGER DEFAULT 0,
                status TEXT DEFAULT 'Ready to Start'
            )
        """)
        self.conn.commit()

    def widgets(self):
        # Homepage
        self.homepage()

    def homepage(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)

        header = ctk.CTkLabel(
            self,
            text="Library",
            font=("Arial", 36, "bold")
        )
        header.grid(row=0, column=0, padx=20, pady=20)

        theme_icon = PhotoImage(file=self.theme_icon_path)
        theme_icon = theme_icon.subsample(10, 10)

        self.switch_theme_button = ctk.CTkButton(
            self,
            text="",
            image=theme_icon,
            command=self.switch_theme,
            height=60,
            width=60,
            fg_color="transparent",
            hover=None
        )
        self.switch_theme_button.grid(row=0, column=10, padx=20, pady=20)

        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()

        if not books:
            no_books_label = ctk.CTkLabel(self, text="No books...")
            no_books_label.grid(row=1, column=0, padx=20, pady=10)
        else:
            center_frame = ctk.CTkFrame(self)
            center_frame.grid(row=2, column=0, columnspan=10, padx=20, pady=20)

            book_no_title = ctk.CTkLabel(center_frame, text="#", font=("Arial", 24))
            book_no_title.grid(row=2, column=0, padx=10, pady=5)

            indexes_to_pass = []

            for i, title_name in enumerate(self.attributes):
                if title_name in ["Publication Year", "Publisher", "ISBN"]:
                    indexes_to_pass.append(i)
                    continue
                title = ctk.CTkLabel(center_frame, text=title_name, font=("Arial", 24))
                title.grid(row=2, column=i+1, padx=10, pady=5)

            for i, book in enumerate(books, start=1):
                index = ctk.CTkLabel(center_frame, text=i, font=("Arial", 12))
                index.grid(row=i+2, column=0, padx=10, pady=5)

                for j, attribute in enumerate(book[1:], start=1):
                    if j-1 in indexes_to_pass:
                        continue
                    attribute_label = ctk.CTkLabel(center_frame, text=attribute, font=("Arial", 12))
                    attribute_label.grid(row=i+2, column=j, padx=10, pady=5)

                delete_icon = PhotoImage(file=self.delete_icon_path)
                delete_icon = delete_icon.subsample(20, 20)

                delete_button = ctk.CTkButton(
                    center_frame,
                    image=delete_icon,
                    text="",
                    command=lambda book_id=book[0]: self.delete_book(book_id),
                    fg_color="red",
                    hover_color="darkred",
                    width=20,
                    height=20,
                    corner_radius=10
                )
                delete_button.grid(row=i+2, column=j+1, padx=10, pady=5)

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

        self.add_book_button.grid(row=len(books)+3, column=0, padx=20, pady=10)

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

        for i, attr in enumerate(self.attributes[:7]):
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
        
        page_count = book_data["Page Count"]
        if not page_count.isdigit():
            messagebox.showerror("Invalid Input", "Page Count must be a valid Integer.")
            return
        
        self.cursor.execute("""
            INSERT INTO books (book_name, author_name, publication_year, publisher, genre, isbn, page_count)
            VALUES (:book_name, :author_name, :publication_year, :publisher, :genre, :isbn, :page_count)
        """, {
            "book_name": book_data["Name"],
            "author_name": book_data["Author"],
            "publication_year": book_data["Publication Year"],
            "publisher": book_data["Publisher"],
            "genre": book_data["Genre"],
            "isbn": book_data["ISBN"],
            "page_count": book_data["Page Count"]
        })
        self.conn.commit()

        messagebox.showinfo("Success", "Book saved.")

        for entry in self.entries.values():
            entry.delete(0, END)

    def delete_book(self, book_id):
        confirm = messagebox.askyesno("Delete Book", "Are you sure you want to delete this book?")

        if confirm:
            self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Book deleted successfully.")
            self.homepage()

    def switch_theme(self):
        if self.current_theme == "dark":
            ctk.set_appearance_mode("light")
            self.current_theme = "light"
        else:
            ctk.set_appearance_mode("dark")
            self.current_theme = "dark"

    def _del_(self):
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    app = Library()
    app.mainloop()