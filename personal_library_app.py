import os
from tkinter import *
from tkinter import messagebox
import sqlite3
import customtkinter as ctk
import json

class Library(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x800")
        self.title("My Library")

        ctk.set_default_color_theme("dark-blue")

        self.language = "en"
        self.load_language(self.language)

        self.widget_texts = {} 

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
        self.conn = sqlite3.connect("data/db/library.db")
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

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_rowconfigure(3, weight=3)

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_columnconfigure(2, weight=2)
        main_frame.grid_columnconfigure(3, weight=2)
        main_frame.grid_columnconfigure(4, weight=2)

        header = ctk.CTkLabel(
            main_frame,
            text="My Library",
            font=("Arial", 36, "bold")
        )
        header.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        self.library_page_button = ctk.CTkButton(
            main_frame,
            # image=library_icon,
            text="My Library",
            command=self.library_page,
        )
        self.library_page_button.grid(row=0, column=2, padx=20, pady=20, sticky="ne")

        self.stats_button = ctk.CTkButton(
            main_frame,
            # image=stats_icon,
            text="Stats",
            command=self.stats_page,
        )
        self.stats_button.grid(row=0, column=3, padx=20, pady=20, sticky="ne")

        self.settings_button = ctk.CTkButton(
            main_frame,
            # image=settings_icon,
            text="Settings",
            command=self.settings_page,
        )
        self.settings_button.grid(row=0, column=4, padx=20, pady=20, sticky="ne")

        self.page_question_label = ctk.CTkLabel(
            main_frame,
            text="How many pages have you read today?",
            font=("Arial", 20, "italic")
        )
        self.page_question_label.grid(row=1, column=1, columnspan=3, padx=20, pady=5, sticky="nsew")

        add_icon = PhotoImage(file=self.add_icon_path)
        add_icon = add_icon.subsample(10, 10)

        self.add_pages_button = ctk.CTkButton(
            main_frame,
            image=add_icon,
            text="",
            command=self.add_pages_page,
            fg_color="transparent",
            hover=None
        )
        self.add_pages_button.grid(row=2, column=1, columnspan=3, padx=20, pady=5, sticky="nsew")

        self.information_label = ctk.CTkLabel(
            main_frame,
            text="Last time, you were on page x of the book x.",
            font=("Arial", 20)
        )
        self.information_label.grid(row=3, column=1, columnspan=3, padx=20, pady=20, sticky="nsew")

    def library_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        main_frame.grid_rowconfigure(0, weight=0)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(
            main_frame,
            text="Library",
            font=("Arial", 36, "bold")
        )
        header.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        self.homepage_button = ctk.CTkButton(
            main_frame,
            text="Back to Homepage",
            command=self.homepage
        )
        self.homepage_button.grid(row=0, column=1, padx=20, pady=20, sticky="ne")

        center_frame = ctk.CTkFrame(main_frame)
        center_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)

        book_no_title = ctk.CTkLabel(center_frame, text="#", font=("Arial", 24))
        book_no_title.grid(row=0, column=0, padx=10, pady=5)

        indexes_to_pass = []

        for i, title_name in enumerate(self.attributes):
            if title_name in ["Publication Year", "Publisher", "ISBN"]:
                indexes_to_pass.append(i)
                continue
            title = ctk.CTkLabel(center_frame, text=title_name, font=("Arial", 24))
            title.grid(row=0, column=i+1, padx=10, pady=5)

        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()

        if not books:
            no_books_label = ctk.CTkLabel(center_frame, text="No books...")
            no_books_label.grid(row=1, column=0, padx=20, pady=10)
        else:
            for i, book in enumerate(books, start=1):
                index = ctk.CTkLabel(center_frame, text=i, font=("Arial", 12))
                index.grid(row=i, column=0, padx=10, pady=5)

                for j, attribute in enumerate(book[1:], start=1):
                    if j-1 in indexes_to_pass:
                        continue
                    attribute_label = ctk.CTkLabel(center_frame, text=attribute, font=("Arial", 12))
                    attribute_label.grid(row=i, column=j, padx=10, pady=5)

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
                delete_button.grid(row=i, column=j+1, padx=10, pady=5)

        add_icon = PhotoImage(file=self.add_icon_path)
        add_icon = add_icon.subsample(10, 10)

        self.add_book_button = ctk.CTkButton(
            main_frame,
            image=add_icon,
            text="",
            command=self.add_book_page,
            height=35,
            width=35,
            fg_color="transparent",
            hover=None
        )
        self.add_book_button.grid(row=2, column=0, sticky="sw", padx=20, pady=10)

    def stats_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        main_frame.grid_rowconfigure(0, weight=0)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(
            main_frame,
            text="Statistics",
            font=("Arial", 36, "bold")
        )
        header.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        self.homepage_button = ctk.CTkButton(
            main_frame,
            text="Back to Homepage",
            command=self.homepage
        )
        self.homepage_button.grid(row=0, column=1, padx=20, pady=20, sticky="ne")

    def settings_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        main_frame.grid_rowconfigure(0, weight=0)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_rowconfigure(5, weight=1)
        main_frame.grid_rowconfigure(6, weight=1)
        
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_columnconfigure(2, weight=2)
        main_frame.grid_columnconfigure(3, weight=2)
        main_frame.grid_columnconfigure(4, weight=2)
        main_frame.grid_columnconfigure(5, weight=2)
        main_frame.grid_columnconfigure(6, weight=2)
        main_frame.grid_columnconfigure(7, weight=2)
        main_frame.grid_columnconfigure(8, weight=2)
        main_frame.grid_columnconfigure(9, weight=2)

        header = ctk.CTkLabel(
            main_frame,
            text="Settings",
            font=("Arial", 36, "bold")
        )
        header.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        self.homepage_button = ctk.CTkButton(
            main_frame,
            text="Back to Homepage",
            command=self.homepage
        )
        self.homepage_button.grid(row=0, column=9, padx=20, pady=20, sticky="ne")

        set_theme_color_label = ctk.CTkLabel(
            main_frame,
            text="Theme & Color",
            font=("Arial", 24)
        )
        set_theme_color_label.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="w")

        themes = [
            {"text": "Dark", "theme": "dark"},
            {"text": "Light", "theme": "light"},
            {"text": "System", "theme": "system"}
        ]

        theme_label = ctk.CTkLabel(
            main_frame,
            text="Theme",
            font=("Arial", 20)
        )
        theme_label.grid(row=2, column=0, padx=20, pady=0, sticky="w")

        for index, theme in enumerate(themes):
            theme_button = ctk.CTkButton(
                main_frame,
                text=theme["text"],
                command=lambda theme=theme: self.set_theme(theme["theme"]),
                width=30,
                corner_radius=50
            )
            theme_button.grid(row=2, column=index+1, padx=0, pady=0)

        colors = [
            {"text": "Blue", "color": "blue"},
            {"text": "Dark Blue", "color": "dark-blue"},
            {"text": "Green", "color": "green"},
        ]

        color_label = ctk.CTkLabel(
            main_frame,
            text="Color",
            font=("Arial", 20)
        )
        color_label.grid(row=3, column=0, padx=20, pady=0, sticky="w")

        for index, color in enumerate(colors):
            color_button = ctk.CTkButton(
                main_frame,
                text=color["text"],
                command=lambda color=color: self.set_color(color["color"]),
                width=30,
                corner_radius=50
            )
            color_button.grid(row=3, column=index+1, padx=0, pady=0)

        goals_label = ctk.CTkLabel(
            main_frame,
            text="Page Goals",
            font=("Arial", 24)
        )
        goals_label.grid(row=4, column=0, padx=20, pady=0, sticky="w")

        validate_cmd = (main_frame.register(self.validate_input), "%P")

        self.widget_texts["daily_goal_label"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("daily_goal_label"),
            font=("Arial", 20)
        )
        self.widget_texts["daily_goal_label"].grid(row=5, column=0, padx=20, pady=0, sticky="w")

        daily_goal_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="...",
            validate="key",
            validatecommand=validate_cmd
        )
        daily_goal_entry.grid(row=5, column=1, columnspan=2, padx=20, pady=0, sticky="w")

        self.widget_texts["weekly_goal_label"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("weekly_goal_label"),
            font=("Arial", 20)
        )
        self.widget_texts["weekly_goal_label"].grid(row=6, column=0, padx=20, pady=0, sticky="w")
        
        weekly_goal_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="...",
            validate="key",
            validatecommand=validate_cmd
        )
        weekly_goal_entry.grid(row=6, column=1, columnspan=2, padx=20, pady=0, sticky="w")

        self.widget_texts["change_language_button"] = ctk.CTkButton(
            main_frame, 
            text=self.get_text("change_language_button"), 
            command=self.change_language
        )
        self.widget_texts["change_language_button"].grid(row=7, column=0, padx=20, pady=20)

    def add_pages_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=0, column=0, padx=20, pady=20)

        # header = ctk.CTkLabel(
        #     center_frame,
        #     text="Add Record",
        #     font=("Arial", 24, "bold")
        # )
        # header.grid(row=0, column=0, columnspan=2, pady=20)

        pages_label = ctk.CTkLabel(center_frame, text="Pages")
        pages_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        pages_entry = ctk.CTkEntry(center_frame, placeholder_text="...")
        pages_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        book_list = self.get_books_from_db()

        book_label = ctk.CTkLabel(center_frame, text="Book")
        book_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        book_combobox = ctk.CTkComboBox(center_frame, values=book_list)
        book_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        save_button = ctk.CTkButton(
            center_frame,
            text="Add Record",
            # command=self.save_book,
            fg_color="darkgreen"
        )
        save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        back_button = ctk.CTkButton(
            center_frame,
            text="Back",
            command=self.homepage,
            fg_color="darkred"
        )
        back_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

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
            command=self.library_page,
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

    def get_books_from_db(self):
        conn = sqlite3.connect("data/db/library.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT book_name FROM books")
        books = cursor.fetchall()

        conn.close()
        
        return [book[0] for book in books]

    def delete_book(self, book_id):
        confirm = messagebox.askyesno("Delete Book", "Are you sure you want to delete this book?")

        if confirm:
            self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Book deleted successfully.")
            self.library_page()

    def validate_input(self, P):
        if P == "" or (P.isdigit() and len(P) <= 4):
            return True
        else:
            return False

    def set_theme(self, theme):
        ctk.set_appearance_mode(theme)

    def set_color(self, color):
        ctk.set_default_color_theme(color)

        return self.settings_page()

    def _del_(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    def load_language(self, lang_code):
        with open("data/languages/language.json", "r", encoding="utf-8") as file:
            self.languages = json.load(file)
        self.language = lang_code

    def get_text(self, key):
        return self.languages.get(self.language, {}).get(key, key)

    def change_language(self):
        if self.language == 'en':
                    self.language = 'tr'
        else:
            self.language = 'en'

        self.load_language(self.language)
        
        for widget_key, widget in self.widget_texts.items():
            widget.configure(text=self.get_text(widget_key))

if __name__ == "__main__":
    app = Library()
    app.mainloop()