import os
from tkinter import *
from tkinter import messagebox
import sqlite3
import customtkinter as ctk
import json
from datetime import datetime, timedelta

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
        self.edit_icon_path = os.path.join(BASE_DIR, "icons/edit_icon.png")
        self.delete_icon_path = os.path.join(BASE_DIR, "icons/delete_icon.png")
        self.take_note_icon_path = os.path.join(BASE_DIR, "icons/take_note_icon.png")
        self.go_back_icon_path = os.path.join(BASE_DIR, "icons/go_back_icon.png")

        # Settings
        self.english_icon_path = os.path.join(BASE_DIR, "icons/languages/english_icon.png")
        self.turkish_icon_path = os.path.join(BASE_DIR, "icons/languages/turkish_icon.png")
        self.german_icon_path = os.path.join(BASE_DIR, "icons/languages/german_icon.png")

        self.attributes = ["Name", "Author", "Publication Year", "Publisher", "Genre", "ISBN", "Page Count", "Pages Read", "Status"]

        self.entries = {}
        self.entries_edit = {}

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

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                tag TEXT,
                date DATE
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

        for i in range(5):
            if i == 3:
                main_frame.grid_rowconfigure(i, weight=3)
            else:
                main_frame.grid_rowconfigure(i, weight=1)

        for i in range(5):
            if i == 0:
                main_frame.grid_columnconfigure(i, weight=1)
            else:
                main_frame.grid_columnconfigure(i, weight=2)

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

        with open("data/settings.json", "r") as settings_file:
            settings = json.load(settings_file)

        daily_goal = settings.get("daily_goal", "goal")
        weekly_goal = settings.get("weekly_goal", "goal")
        monthly_goal = settings.get("monthly_goal", "goal")

        last_read_book = settings.get("last_read_book", "book")

        last_read_page = self.cursor.execute("""
            SELECT pages_read 
            FROM books 
            WHERE book_name = :book
        """, {
            "book": last_read_book
        }).fetchone()
        last_read_page = str(last_read_page[0]) if last_read_page else "0"

        information_label_text = self.get_text("information_label").format(
            book=last_read_book,
            page=last_read_page,
        )

        self.widget_texts["information_label"] = ctk.CTkLabel(
            main_frame,
            text=information_label_text,
            font=("Arial", 20)
        )
        self.widget_texts["information_label"].grid(row=3, column=1, columnspan=3, padx=20, pady=20, sticky="nsew")

        today = datetime.now()
        start_of_day = today.strftime("%Y-%m-%d 00:00:00")
        
        start_of_week_date = today - timedelta(days=today.weekday())
        start_of_week = start_of_week_date.strftime("%Y-%m-%d 00:00:00")

        start_of_month_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_of_month = start_of_month_date.strftime("%Y-%m-%d %H:%M:%S") 

        start_of_year_date = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        start_of_year = start_of_year_date.strftime("%Y-%m-%d %H:%M:%S")

        self.daily_read_pages = self.calculate_pages_read(self.cursor, start_of_day)
        self.weekly_read_pages = self.calculate_pages_read(self.cursor, start_of_week)
        self.monthly_read_pages = self.calculate_pages_read(self.cursor, start_of_month)
        self.yearly_read_pages = self.calculate_pages_read(self.cursor, start_of_year)

        self.widget_texts["daily_goal_progress"] = ctk.CTkLabel(
            main_frame,
            text=str(self.daily_read_pages) + "/" + str(daily_goal) + "\n\n" + self.get_text("daily_goal_label"),
            font=("Arial", 15)
        )
        self.widget_texts["daily_goal_progress"].grid(row=4, column=1, padx=20, pady=20, sticky="nsew")

        self.widget_texts["weekly_goal_progress"] = ctk.CTkLabel(
            main_frame,
            text=str(self.weekly_read_pages) + "/" + str(weekly_goal) + "\n\n" + self.get_text("weekly_goal_label"),
            font=("Arial", 15)
        )
        self.widget_texts["weekly_goal_progress"].grid(row=4, column=2, padx=20, pady=20, sticky="nsew")

        self.widget_texts["monthly_goal_progress"] = ctk.CTkLabel(
            main_frame,
            text=str(self.monthly_read_pages) + "/" + str(monthly_goal) + "\n\n" + self.get_text("monthly_goal_label"),
            font=("Arial", 15)
        )
        self.widget_texts["monthly_goal_progress"].grid(row=4, column=3, padx=20, pady=20, sticky="nsew")

    def calculate_pages_read(self, cursor, start_date):
        query = """
            SELECT pages_read
            FROM reading_logs
            WHERE date >= :start_date
        """
        rows = cursor.execute(query, {"start_date": start_date}).fetchall()
        return sum(int(row[0]) for row in rows)

    def library_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = ctk.CTkScrollableFrame(self)
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
            command=self.notes_page
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

                edit_icon = PhotoImage(file=self.edit_icon_path)
                edit_icon = edit_icon.subsample(20, 20)

                edit_button = ctk.CTkButton(
                    center_frame,
                    image=edit_icon,
                    text="",
                    command=lambda book_id=book[0]: self.edit_book_page(book_id),
                    fg_color="green",
                    hover_color="darkgreen",
                    width=10,
                    height=10,
                    corner_radius=10
                )
                edit_button.grid(row=i, column=j+1, padx=10, pady=5)

                delete_icon = PhotoImage(file=self.delete_icon_path)
                delete_icon = delete_icon.subsample(20, 20)

                delete_button = ctk.CTkButton(
                    center_frame,
                    image=delete_icon,
                    text="",
                    command=lambda book_id=book[0]: self.delete_book(book_id),
                    fg_color="red",
                    hover_color="darkred",
                    width=10,
                    height=10,
                    corner_radius=10
                )
                delete_button.grid(row=i, column=j+2, padx=10, pady=5)

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

    def edit_book_page(self, book_id):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        book = self.cursor.execute("""
            SELECT * 
            FROM books
            WHERE id = :book_id
        """, {
            "book_id": book_id
        }).fetchone()
        print(book)
        
        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=0, column=0, padx=20, pady=20)

        self.widget_texts["edit_book_header"] = ctk.CTkLabel(
            center_frame,
            text=self.get_text("edit_book_header"),
            font=("Arial", 24, "bold")
        )
        self.widget_texts["edit_book_header"].grid(row=0, column=0, columnspan=2, pady=20)

        for i, attr in enumerate(self.attributes[:8]):
            placeholder = book[i+1]
            self.create_label_and_entry_in_frame_edit_page(center_frame, attr, placeholder, row=i+1)

        self.widget_texts["save_book_button"] = ctk.CTkButton(
            center_frame,
            text=self.get_text("save_book_button"),
            command=lambda: self.edit_book(book_id),
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

    def edit_book(self, book_id):
        book_data = {key: entry.get() for key, entry in self.entries_edit.items()}

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
            UPDATE books
            SET book_name = :book_name, author_name = :author_name, 
            publication_year = :publication_year, publisher = :publisher, 
            genre = :genre, isbn = :isbn, page_count = :page_count, pages_read = :pages_read
            WHERE id = :id
        """, {
            "book_name": book_data["Name"],
            "author_name": book_data["Author"],
            "publication_year": book_data["Publication Year"],
            "publisher": book_data["Publisher"],
            "genre": book_data["Genre"],
            "isbn": book_data["ISBN"],
            "page_count": book_data["Page Count"],
            "pages_read": book_data["Pages Read"],
            "id": book_id
        })
        self.conn.commit()

        messagebox.showinfo(
            self.get_text("success_title"),
            self.get_text("success_message")
        )

        self.library_page()

    def notes_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = ctk.CTkScrollableFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # main_frame.grid_rowconfigure(0, weight=0)
        # main_frame.grid_rowconfigure(1, weight=1)

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)

        self.widget_texts["notes_header"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("notes_header"),
            font=("Arial", 36, "bold")
        )
        self.widget_texts["notes_header"].grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        go_back_icon = PhotoImage(file=self.go_back_icon_path)
        go_back_icon = go_back_icon.subsample(12, 12)

        self.widget_texts["library_page_button"] = ctk.CTkButton(
            main_frame,
            image=go_back_icon,
            text="",
            # text=self.get_text("library_page_button"),
            command=self.library_page
        )
        self.widget_texts["library_page_button"].grid(row=0, column=2, padx=20, pady=20, sticky="ne")

        add_icon = PhotoImage(file=self.add_icon_path)
        add_icon = add_icon.subsample(12, 12)

        self.add_note_button = ctk.CTkButton(
            main_frame,
            image=add_icon,
            text="",
            command=self.add_note_page,
            height=35,
            width=35,
            fg_color="transparent",
            hover=None
        )
        self.add_note_button.grid(row=1, column=0, sticky="w", padx=20, pady=20)

        self.cursor.execute("SELECT * FROM notes")
        notes = self.cursor.fetchall()

        for i, note in enumerate(notes):
            date_label = ctk.CTkLabel(
                main_frame,
                text=note[4],
                font=("Helvetica", 14, "bold"),
                # width=100
            )
            date_label.grid(row=i * 5 + 2, column=0, padx=(20, 0), pady=(20, 5), sticky="w")

            title_label = ctk.CTkLabel(
                main_frame,
                text=self.get_text("note_title") + ":",
                # width=100
            )
            title_label.grid(row=i * 5 + 3, column=0, padx=(20, 0), pady=5, sticky="w")

            title_entry = ctk.CTkEntry(
                main_frame,
                corner_radius=5,
                width=400
            )
            title_entry.insert(0, note[1])
            title_entry.grid(row=i * 5 + 3, column=1, padx=10, pady=5, sticky="w")

            content_label = ctk.CTkLabel(
                main_frame,
                text=self.get_text("note_content") + ":",
                # width=100
            )
            content_label.grid(row=i * 5 + 4, column=0, padx=(20, 0), pady=5, sticky="w")

            self.content_update_textbox = ctk.CTkTextbox(
                main_frame,
                corner_radius=5,
                width=400,
                height=100
            )
            self.content_update_textbox.insert("0.0", note[2])
            self.content_update_textbox.grid(row=i * 5 + 4, column=1, padx=10, pady=5, sticky="w")

            tag_label = ctk.CTkLabel(
                main_frame,
                text=self.get_text("note_tag") + ":",
                # width=100
            )
            tag_label.grid(row=i * 5 + 5, column=0, padx=(20, 0), pady=5, sticky="w")

            tag_entry = ctk.CTkEntry(
                main_frame,
                corner_radius=5,
                width=400
            )
            tag_entry.insert(0, note[3])
            tag_entry.grid(row=i * 5 + 5, column=1, padx=10, pady=5, sticky="w")

            save_button = ctk.CTkButton(
                main_frame,
                text=self.get_text("save_button"),
                command=lambda t=title_entry, tg=tag_entry, n_id=note[0]: self.update_note(t, tg, n_id),
                fg_color="green",
                width=100
            )
            save_button.grid(row=i * 5 + 6, column=0, padx=10, pady=10, sticky="w")

            delete_note_button = ctk.CTkButton(
                main_frame,
                text=self.get_text("delete_note_title"),
                command=lambda n_id=note[0]: self.delete_note(n_id),
                fg_color="darkred",
                width=100
            )
            delete_note_button.grid(row=i * 5 + 6, column=0, padx=0, pady=10, sticky="e")

    def update_note(self, title_entry, tag_entry, id):
        title = title_entry.get()
        content = self.content_update_textbox.get("0.0", "end-1c")
        tag = tag_entry.get()

        self.cursor.execute("""
            UPDATE notes
            SET title = :title, content = :content, tag = :tag
            WHERE id = :id
        """, {
            "title": title,
            "content": content,
            "tag": tag,
            "id": id
        })
        self.conn.commit()

        messagebox.showinfo(
            self.get_text("success_title"),
            self.get_text("note_success_message")
        )
    
    def add_note_page(self):
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

        self.widget_texts["note_title"] = ctk.CTkLabel(
            center_frame,
            text=self.get_text("note_title"),
            font=("Helvetica", 14, "bold")
        )
        self.widget_texts["note_title"].grid(row=0, column=0, padx=20, pady=(10, 5), sticky="w")

        self.note_title_entry = ctk.CTkEntry(
            center_frame,
            width=200,
        )
        self.note_title_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=(10, 5), sticky="w")

        # self.note_content_entry = ctk.CTkEntry(
        #     center_frame,
        #     placeholder_text=self.get_text("note_content"),
        #     width=300,
        #     height=50
        # )
        self.widget_texts["note_content"] = ctk.CTkLabel(
            center_frame,
            text=self.get_text("note_content"),
            font=("Helvetica", 14, "bold")
        )
        self.widget_texts["note_content"].grid(row=2, column=0, padx=20, pady=(10, 5), sticky="w")

        self.note_content_entry = ctk.CTkTextbox(
            center_frame,
            corner_radius=5,
            width=400,
            height=100
        )
        self.note_content_entry.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="w")

        self.widget_texts["note_tag"] = ctk.CTkLabel(
            center_frame,
            text=self.get_text("note_tag"),
            font=("Helvetica", 14, "bold")
        )
        self.widget_texts["note_tag"].grid(row=4, column=0, padx=20, pady=(10, 5), sticky="w")

        self.note_tag_entry = ctk.CTkEntry(
            center_frame,
            width=200,
        )
        self.note_tag_entry.grid(row=5, column=0, columnspan=2, padx=20, pady=5, sticky="w")

        self.widget_texts["note_save_button"] = ctk.CTkButton(
            center_frame,
            text=self.get_text("note_save_button"),
            command=lambda: self.save_note(self.note_title_entry.get(), self.note_tag_entry.get()),
            fg_color="darkgreen"
        )
        self.widget_texts["note_save_button"].grid(row=6, column=0, padx=20, pady=10, sticky="w")

        self.widget_texts["back_button"] = ctk.CTkButton(
            center_frame,
            text=self.get_text("back_button"),
            command=self.notes_page,
            fg_color="darkred"
        )
        self.widget_texts["back_button"].grid(row=6, column=1, padx=20, pady=10, sticky="e")

    def save_note(self, title, tag):
        content = self.note_content_entry.get("0.0", "end-1c")

        self.cursor.execute("""
            INSERT INTO notes (title, content, tag, date)
            VALUES (:title, :content, :tag, :date)
        """, {
            "title": title,
            "content": content,
            "tag": tag,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        self.conn.commit()

        messagebox.showinfo(
            self.get_text("success_title"),
            self.get_text("note_success_message")
        )

        self.notes_page()

    def delete_note(self, note_id):
        title_confirm = self.get_text("delete_note_title")
        message_confirm = self.get_text("delete_note_message")
        title_success = self.get_text("delete_success_title")
        message_success = self.get_text("delete_note_success_message")

        confirm = messagebox.askyesno(title_confirm, message_confirm)

        if confirm:
            self.cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            self.conn.commit()
            messagebox.showinfo(title_success, message_success)
            self.notes_page()

    def stats_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        for i in range(9):
            if i == 0:
                main_frame.grid_rowconfigure(i, weight=0)
            else:
                main_frame.grid_rowconfigure(i, weight=2)

        for i in range(10):
            if i == 0:
                main_frame.grid_columnconfigure(i, weight=1)
            else:
                main_frame.grid_columnconfigure(i, weight=2)

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

        self.create_label(main_frame, 1, 0, self.get_text("today") + ":", self.daily_read_pages)
        self.create_label(main_frame, 2, 0, self.get_text("week") + ":", self.weekly_read_pages)
        self.create_label(main_frame, 3, 0, self.get_text("month") + ":", self.monthly_read_pages)
        self.create_label(main_frame, 4, 0, self.get_text("year") + ":", self.yearly_read_pages)

        total_pages_read = self.cursor.execute("SELECT SUM(pages_read) FROM reading_logs").fetchone()[0]
        self.create_label(main_frame, 5, 0, self.get_text("total") + ":", total_pages_read)

    def create_label(self, main_frame, row, column, text, value):
        label_text = ctk.CTkLabel(
            main_frame,
            text=text,
            font=("Arial", 20)
        )
        label_value = ctk.CTkLabel(
            main_frame,
            text=str(value),
            font=("Arial", 20)
        )
        
        label_text.grid(row=row, column=column, padx=20, pady=20, sticky="w")
        label_value.grid(row=row, column=column + 1, padx=20, pady=20, sticky="w")

    def settings_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        main_frame.grid_rowconfigure(0, weight=0)
        main_frame.grid_rowconfigure(1, weight=2)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_rowconfigure(4, weight=2)
        main_frame.grid_rowconfigure(5, weight=1)
        main_frame.grid_rowconfigure(6, weight=1)
        main_frame.grid_rowconfigure(7, weight=1)
        main_frame.grid_rowconfigure(8, weight=1)
        
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

        with open("data/settings.json", "r") as file:
            settings = json.load(file)
            
        daily_goal_placeholder = settings.get("daily_goal", "default")
        weekly_goal_placeholder = settings.get("weekly_goal", "default")
        monthly_goal_placeholder = settings.get("monthly_goal", "default")

        self.widget_texts["daily_goal_label"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("daily_goal_label"),
            font=("Arial", 20)
        )
        self.widget_texts["daily_goal_label"].grid(row=5, column=0, padx=20, pady=0, sticky="w")

        daily_goal_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text=daily_goal_placeholder,
            validate="key",
            validatecommand=validate_cmd
        )
        daily_goal_entry.insert(0, daily_goal_placeholder)
        daily_goal_entry.grid(row=5, column=1, columnspan=2, padx=20, pady=0, sticky="w")

        self.widget_texts["weekly_goal_label"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("weekly_goal_label"),
            font=("Arial", 20)
        )
        self.widget_texts["weekly_goal_label"].grid(row=6, column=0, padx=20, pady=0, sticky="w")
        
        weekly_goal_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text=weekly_goal_placeholder,
            validate="key",
            validatecommand=validate_cmd
        )
        weekly_goal_entry.insert(0, weekly_goal_placeholder)
        weekly_goal_entry.grid(row=6, column=1, columnspan=2, padx=20, pady=0, sticky="w")

        self.widget_texts["monthly_goal_label"] = ctk.CTkLabel(
            main_frame,
            text=self.get_text("monthly_goal_label"),
            font=("Arial", 20)
        )
        self.widget_texts["monthly_goal_label"].grid(row=7, column=0, padx=20, pady=0, sticky="w")
        
        monthly_goal_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text=monthly_goal_placeholder,
            validate="key",
            validatecommand=validate_cmd
        )
        monthly_goal_entry.insert(0, monthly_goal_placeholder)
        monthly_goal_entry.grid(row=7, column=1, columnspan=2, padx=20, pady=0, sticky="w")

        self.widget_texts["save_goals_button"] = ctk.CTkButton(
            main_frame, 
            text=self.get_text("save_button"), 
            command=lambda: self.save_goals(daily_goal_entry.get(), weekly_goal_entry.get(), monthly_goal_entry.get())
        )
        self.widget_texts["save_goals_button"].grid(row=8, column=0, padx=20, pady=20, sticky="w")

        self.widget_texts["language_label"] = ctk.CTkLabel(
            main_frame, 
            text=self.get_text("language_label"),
            font=("Arial", 20)
        )
        self.widget_texts["language_label"].grid(row=9, column=0, padx=20, pady=20, sticky="w")

        english_icon = PhotoImage(file=self.english_icon_path)
        english_icon = english_icon.subsample(12, 12)

        turkish_icon = PhotoImage(file=self.turkish_icon_path)
        turkish_icon = turkish_icon.subsample(12, 12)

        german_icon = PhotoImage(file=self.german_icon_path)
        german_icon = german_icon.subsample(12, 12)

        english_button = ctk.CTkButton(
            main_frame, 
            text="", 
            image=english_icon,
            command=lambda: self.change_language("en"),
            fg_color="transparent",
            hover=None
        )
        english_button.grid(row=9, column=1, padx=20, pady=20, sticky="w")

        turkish_button = ctk.CTkButton(
            main_frame, 
            text="", 
            image=turkish_icon,
            command=lambda: self.change_language("tr"),
            fg_color="transparent",
            hover=None
        )
        turkish_button.grid(row=9, column=2, padx=20, pady=20, sticky="w")

        german_button = ctk.CTkButton(
            main_frame, 
            text="", 
            image=german_icon,
            command=lambda: self.change_language("de"),
            fg_color="transparent",
            hover=None
        )
        german_button.grid(row=9, column=3, padx=20, pady=20, sticky="w")

    def add_pages_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=0, column=0, padx=20, pady=20)

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

            self.cursor.execute("""
                INSERT INTO reading_logs (book_name, pages_read, date)
                VALUES (:book_name, :pages_read, :date)
            """, {
                "book_name": book_name,
                "pages_read": pages_read,
                "date": datetime.now()
            })
            self.conn.commit()

            try:
                with open("data/settings.json", "r") as settings_file:
                    settings = json.load(settings_file)
                settings["last_read_book"] = book_name

                with open("data/settings.json", "w") as settings_file:
                    json.dump(settings, settings_file, indent=4)

            except FileNotFoundError:
                messagebox.showerror(self.get_text("error_title"), self.get_text("settings_file_not_found"))
            except json.JSONDecodeError:
                messagebox.showerror(self.get_text("error_title"), self.get_text("error_parsing_json"))

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

    def create_label_and_entry_in_frame_edit_page(self, frame, text, placeholder, row):
        label = ctk.CTkLabel(frame, text=self.get_text(text))
        label.grid(row=row, column=0, padx=10, pady=10, sticky="e")

        entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
        entry.insert(0, placeholder)
        entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")

        self.entries_edit[text] = entry

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

    def save_goals(self, daily, weekly, monthly):
        daily_goal = daily
        weekly_goal = weekly
        monthly_goal = monthly

        settings = self.load_settings()
        settings["daily_goal"] = daily_goal
        settings["weekly_goal"] = weekly_goal
        settings["monthly_goal"] = monthly_goal

        with open("data/settings.json", "w") as file:
            json.dump(settings, file, indent=4)

        self.settings_page()

    def change_language(self, language):
        self.language = language

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