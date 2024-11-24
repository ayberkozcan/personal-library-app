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

        settings = self.load_settings()
        self.current_theme = settings.get("theme")
        self.current_color = settings.get("color")
        self.language = settings.get("language")

        ctk.set_appearance_mode(self.current_theme)
        ctk.set_default_color_theme(self.current_color)
        self.load_language(self.language)

        self.widget_texts = {} 
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # Homepage
        self.homepage_icon_path = os.path.join(BASE_DIR, "icons/homepage_icon.png")
        self.library_icon_path = os.path.join(BASE_DIR, "icons/library_icon.png")
        self.stats_icon_path = os.path.join(BASE_DIR, "icons/stats_icon.png")
        self.settings_icon_path = os.path.join(BASE_DIR, "icons/settings_icon.png")

        self.theme_icon_path = os.path.join(BASE_DIR, "icons/theme_icon.png")

        # Library
        self.add_icon_path = os.path.join(BASE_DIR, "icons/add_icon.png")
        self.delete_icon_path = os.path.join(BASE_DIR, "icons/delete_icon.png")
        self.take_note_icon_path = os.path.join(BASE_DIR, "icons/take_note_icon.png")

        self.attributes = ["Name", "Author", "Publication Year", "Publisher", "Genre", "ISBN", "Page Count", "Pages Read", "Status"]

        self.entries = {}

        self.connect_database()

        self.widgets()

    def load_settings(self):
        try:
            with open("data/settings.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"theme": "dark", "color": "dark-blue", "language": "en"}

    def connect_database(self):
        self.conn = sqlite3.connect("data/database/library.db")
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

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reading_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_name INTEGER,
                pages_read INTEGER,
                date DATE,
                FOREIGN KEY (book_name) REFERENCES books (book_name)
            )
        """)

        self.conn.commit()

    def widgets(self):
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

        self.widget_texts["homepage_header"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("homepage_header"),
            font=("Arial", 36, "bold")
        )
        self.widget_texts["homepage_header"].grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        library_icon = PhotoImage(file=self.library_icon_path)
        library_icon = library_icon.subsample(12, 12)

        self.widget_texts["library_page_button"] = ctk.CTkButton(
            main_frame,
            image=library_icon,
            text="",
            # text=self.get_text("library_page_button"),
            command=self.library_page,
        )
        self.widget_texts["library_page_button"].grid(row=0, column=2, padx=20, pady=20, sticky="ne")

        stats_icon = PhotoImage(file=self.stats_icon_path)
        stats_icon = stats_icon.subsample(12, 12)

        self.widget_texts["stats_button"] = ctk.CTkButton(
            main_frame,
            image=stats_icon,
            text="",
            # text=self.get_text("stats_button"),
            command=self.stats_page,
        )
        self.widget_texts["stats_button"].grid(row=0, column=3, padx=20, pady=20, sticky="ne")

        settings_icon = PhotoImage(file=self.settings_icon_path)
        settings_icon = settings_icon.subsample(12, 12)

        self.widget_texts["settings_button"] = ctk.CTkButton(
            main_frame,
            image=settings_icon,
            text="",
            # text=self.get_text("settings_button"),
            command=self.settings_page,
        )
        self.widget_texts["settings_button"].grid(row=0, column=4, padx=20, pady=20, sticky="ne")

        self.widget_texts["page_question_label"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("page_question_label"),
            font=("Arial", 20, "italic")
        )
        self.widget_texts["page_question_label"].grid(row=1, column=1, columnspan=3, padx=20, pady=5, sticky="nsew")

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

        self.widget_texts["information_label"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("information_label"),
            font=("Arial", 20)
        )
        self.widget_texts["information_label"].grid(row=3, column=1, columnspan=3, padx=20, pady=20, sticky="nsew")

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

        self.widget_texts["library_header"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("library_header"),
            font=("Arial", 36, "bold")
        )
        self.widget_texts["library_header"].grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        take_note_icon = PhotoImage(file=self.take_note_icon_path)
        take_note_icon = take_note_icon.subsample(12, 12)

        self.widget_texts["take_note_button"] = ctk.CTkButton(
            main_frame,
            image=take_note_icon,
            text="",
            # text=self.get_text("take_note_button"),
            # command=self.note_page
        )
        self.widget_texts["take_note_button"].grid(row=0, column=1, padx=20, pady=20, sticky="ne")

        homepage_icon = PhotoImage(file=self.homepage_icon_path)
        homepage_icon = homepage_icon.subsample(12, 12)

        self.widget_texts["homepage_button"] = ctk.CTkButton(
            main_frame,
            image=homepage_icon,
            text="",
            # text=self.get_text("homepage_button"),
            command=self.homepage
        )
        self.widget_texts["homepage_button"].grid(row=0, column=2, padx=20, pady=20, sticky="ne")

        center_frame = ctk.CTkFrame(main_frame)
        center_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)

        book_no_title = ctk.CTkLabel(
            center_frame, 
            text="#", 
            font=("Arial", 24)
        )
        book_no_title.grid(row=0, column=0, padx=10, pady=5)

        indexes_to_pass = []

        for i, title_name in enumerate(self.attributes):
            if title_name in ["Publication Year", "Publisher", "ISBN"]:
                indexes_to_pass.append(i)
                continue
            title = ctk.CTkLabel(
                center_frame, 
                text=self.get_text(title_name), 
                font=("Arial", 24)
            )
            title.grid(row=0, column=i+1, padx=10, pady=5)

        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()

        if not books:
            self.widget_texts["no_books_label"] = ctk.CTkLabel(
                center_frame, 
                text=self.get_text("no_books_label"),
                font=("Arial", 20, "italic")
            )
            self.widget_texts["no_books_label"].grid(row=1, column=0, padx=20, pady=10)
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

        self.widget_texts["stats_header"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("stats_header"),
            font=("Arial", 36, "bold")
        )
        self.widget_texts["stats_header"].grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        homepage_icon = PhotoImage(file=self.homepage_icon_path)
        homepage_icon = homepage_icon.subsample(12, 12)

        self.widget_texts["homepage_button"] = ctk.CTkButton(
            main_frame,
            image=homepage_icon,
            text="",
            # text=self.get_text("homepage_button"),
            command=self.homepage
        )
        self.widget_texts["homepage_button"].grid(row=0, column=1, padx=20, pady=20, sticky="ne")

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

        self.widget_texts["settings_header"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("settings_header"),
            font=("Arial", 36, "bold")
        )
        self.widget_texts["settings_header"].grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        homepage_icon = PhotoImage(file=self.homepage_icon_path)
        homepage_icon = homepage_icon.subsample(12, 12)

        self.widget_texts["homepage_button"] = ctk.CTkButton(
            main_frame,
            image=homepage_icon,
            text="",
            # text=self.get_text("homepage_button"),
            command=self.homepage
        )
        self.widget_texts["homepage_button"].grid(row=0, column=9, padx=20, pady=20, sticky="ne")

        self.widget_texts["set_theme_color_label"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("set_theme_color_label"),
            font=("Arial", 24)
        )
        self.widget_texts["set_theme_color_label"].grid(row=1, column=0, padx=20, pady=(20, 0), sticky="w")

        themes = [
            {"text": self.get_text("dark"), "theme": "dark"},
            {"text": self.get_text("light"), "theme": "light"},
            {"text": self.get_text("system"), "theme": "system"}
        ]

        self.widget_texts["theme_label"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("theme_label"),
            font=("Arial", 20)
        )
        self.widget_texts["theme_label"].grid(row=2, column=0, padx=20, pady=0, sticky="w")

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
            {"text": self.get_text("blue"), "color": "blue"},
            {"text": self.get_text("dark-blue"), "color": "dark-blue"},
            {"text": self.get_text("green"), "color": "green"},
        ]

        self.widget_texts["color_label"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("color_label"),
            font=("Arial", 20)
        )
        self.widget_texts["color_label"].grid(row=3, column=0, padx=20, pady=0, sticky="w")

        for index, color in enumerate(colors):
            color_button = ctk.CTkButton(
                main_frame,
                text=color["text"],
                command=lambda color=color: self.set_color(color["color"]),
                width=30,
                corner_radius=50
            )
            color_button.grid(row=3, column=index+1, padx=0, pady=0)

        self.widget_texts["goals_label"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("goals_label"),
            font=("Arial", 24)
        )
        self.widget_texts["goals_label"].grid(row=4, column=0, padx=20, pady=0, sticky="w")

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
        self.widget_texts["change_language_button"].grid(row=7, column=0, padx=20, pady=20, sticky="w")

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

        validate_cmd = (center_frame.register(self.validate_input), "%P")

        book_list = self.get_books_from_db()

        self.widget_texts["book_label"] = ctk.CTkLabel(
            center_frame, 
            text=self.get_text("book_label")
        )
        self.widget_texts["book_label"].grid(row=0, column=0, padx=10, pady=10, sticky="e")

        book_combobox = ctk.CTkComboBox(
            center_frame, 
            values=book_list
        )
        book_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.widget_texts["pages_label"] = ctk.CTkLabel(
            center_frame, 
            text=self.get_text("pages_label"),
        )
        self.widget_texts["pages_label"].grid(row=1, column=0, padx=10, pady=10, sticky="e")

        pages_entry = ctk.CTkEntry(
            center_frame, 
            placeholder_text="...",
            validate="key",
            validatecommand=validate_cmd
        )
        pages_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.widget_texts["save_record_button"] = ctk.CTkButton(
            center_frame,
            text=self.get_text("save_record_button"),
            command=lambda: self.save_reading_log(book_combobox.get(), pages_entry.get()),
            fg_color="darkgreen"
        )
        self.widget_texts["save_record_button"].grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.widget_texts["back_button"] = ctk.CTkButton(
            center_frame,
            text=self.get_text("back_button"),
            command=self.homepage,
            fg_color="darkred"
        )
        self.widget_texts["back_button"].grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def save_reading_log(self, book_name, pages_read):
        pages_read = int(pages_read)

        if pages_read > 0:
            self.cursor.execute(
                "UPDATE books SET pages_read = pages_read + ? WHERE book_name = ?",
                (pages_read, book_name)
            )
            self.conn.commit()

            messagebox.showinfo(self.get_text("success_title"), f"{pages_read}" + self.get_text("pages_added"))

            self.homepage()
        else:
            messagebox.showerror(
                self.get_text("error_title"),
                self.get_text("error_page_count")
            )
            
    def add_book_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=0, column=0, padx=20, pady=20)

        self.widget_texts["add_book_header"] = ctk.CTkLabel(
            center_frame,
            text=self.get_text("add_book_header"),
            font=("Arial", 24, "bold")
        )
        self.widget_texts["add_book_header"].grid(row=0, column=0, columnspan=2, pady=20)

        for i, attr in enumerate(self.attributes[:7]):
            self.create_label_and_entry_in_frame(center_frame, attr, row=i+1)

        self.widget_texts["save_book_button"] = ctk.CTkButton(
            center_frame,
            text=self.get_text("save_book_button"),
            command=self.save_book,
            fg_color="darkgreen"
        )
        self.widget_texts["save_book_button"].grid(row=len(self.attributes)+1, column=0, columnspan=2, padx=10, pady=10)

        self.widget_texts["back_button"] = ctk.CTkButton(
            center_frame,
            text=self.get_text("back_button"),
            command=self.library_page,
            fg_color="darkred"
        )
        self.widget_texts["back_button"].grid(row=len(self.attributes)+2, column=0, columnspan=2, padx=10, pady=10)

    def create_label_and_entry_in_frame(self, frame, text, row):
        label = ctk.CTkLabel(frame, text=self.get_text(text))
        label.grid(row=row, column=0, padx=10, pady=10, sticky="e")

        entry = ctk.CTkEntry(frame, placeholder_text="...")
        entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")

        self.entries[text] = entry

    def save_book(self):
        book_data = {key: entry.get() for key, entry in self.entries.items()}

        publication_year = book_data["Publication Year"]
        if not publication_year.isdigit():
            messagebox.showerror(
                self.get_text("error_title"),
                self.get_text("error_publication_year")
            )
            return

        isbn = book_data["ISBN"]
        if not isbn.isdigit():
            messagebox.showerror(
                self.get_text("error_title"),
                self.get_text("error_isbn")
            )
            return

        page_count = book_data["Page Count"]
        if not page_count.isdigit():
            messagebox.showerror(
                self.get_text("error_title"),
                self.get_text("error_page_count")
            )
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

        messagebox.showinfo(
            self.get_text("success_title"),
            self.get_text("success_message")
        )

        for entry in self.entries.values():
            entry.delete(0, END)

    def get_books_from_db(self):
        conn = sqlite3.connect("data/database/library.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT book_name FROM books")
        books = cursor.fetchall()

        conn.close()
        
        return [book[0] for book in books]

    def delete_book(self, book_id):
        title_confirm = self.get_text("delete_book_title")
        message_confirm = self.get_text("delete_book_message")
        title_success = self.get_text("delete_success_title")
        message_success = self.get_text("delete_success_message")

        confirm = messagebox.askyesno(title_confirm, message_confirm)

        if confirm:
            self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            self.conn.commit()
            messagebox.showinfo(title_success, message_success)
            self.library_page()

    def validate_input(self, P):
        if P == "" or (P.isdigit() and len(P) <= 4):
            return True
        else:
            return False

    def set_theme(self, theme):
        ctk.set_appearance_mode(theme)

        settings = self.load_settings()
        settings["theme"] = theme

        with open("data/settings.json", "w") as file:
            json.dump(settings, file, indent=4)
        
        self.current_theme = theme

    def set_color(self, color):
        ctk.set_default_color_theme(color)

        settings = self.load_settings()
        settings["color"] = color

        with open("data/settings.json", "w") as file:
            json.dump(settings, file, indent=4)

        return self.settings_page()

    def _del_(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    def load_language(self, lang_code):
        with open("data/localization/language.json", "r", encoding="utf-8") as file:
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

        settings = self.load_settings()
        settings["language"] = self.language

        with open("data/settings.json", "w") as file:
            json.dump(settings, file, indent=4)

        self.settings_page()

if __name__ == "__main__":
    app = Library()
    app.mainloop()