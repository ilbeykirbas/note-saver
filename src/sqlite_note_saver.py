import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

class NoteSaver:
    def __init__(self):
        self.selected_id = None # No notes were selected at the start
        self.create_database()
        self.window = tk.Tk()
        self.window.title("SQLite Note Saver")
        
        tk.Label(self.window, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(self.window)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Content:").grid(row=1, column=0, padx=5, pady=5, sticky="ne")
        self.content_text = tk.Text(self.window, width=30, height=8)
        self.content_text.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.window, text="Update", command=self.update).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tk.Button(self.window, text="Save", command=self.save).grid(row=2, column=1, sticky="e")
        tk.Button(self.window, text="Delete", command=self.delete).grid(row=2, column=1, sticky="ns", padx=5, pady=5)
        
        self.info_label = tk.Label(self.window, text="")
        self.info_label.grid(row=3, column=1)

        tk.Label(self.window, text="Saved Notes:").grid(row=0, column=2, padx=5, pady=5)
        self.listbox = tk.Listbox(self.window, width=30)
        self.listbox.grid(row=1, column=2, rowspan=2, padx=5, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.show_note)

        self.info_label = tk.Label(self.window, text="")
        self.info_label.grid(row=3, column=1)

        self.refresh_list()

        self.window.mainloop()
    
    def create_database(self):
        data_folder = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(data_folder, exist_ok=True)  # If the data folder does not exist, create one
        db_path = os.path.join(data_folder, "notes.db")

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )          
        """)
        self.conn.commit()
    
    def save(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()

        if title and content:
            self.cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
            self.conn.commit()
            self.info_label.config(text="Note saved.", fg="green")
            self.title_entry.delete(0, tk.END)
            self.content_text.delete("1.0", tk.END)
            self.refresh_list()
        else:
            self.info_label.config(text="Title and content cannot be empty.", fg="red")
    
    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        self.cursor.execute("SELECT id, title FROM notes")
        self.notes = self.cursor.fetchall()
        for note in self.notes:
            self.listbox.insert(tk.END, f"{note[0]} - {note[1]}")

    def show_note(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.selected_id = self.notes[selected_index[0]][0]
            self.cursor.execute("SELECT title, content FROM notes WHERE id=?", (self.selected_id,))
            data = self.cursor.fetchone()
            if data:
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, data[0])
                self.content_text.delete("1.0", tk.END)
                self.content_text.insert("1.0", data[1])

    def update(self):
        if self.selected_id is not None:
            new_title = self.title_entry.get().strip()
            new_content = self.content_text.get("1.0", tk.END).strip()

            if new_title and new_content:
                self.cursor.execute("UPDATE notes SET title=?, content=? WHERE id=?", 
                                    (new_title, new_content, self.selected_id))
                self.conn.commit()
                self.info_label.config(text="Note updated.", fg="green")
                self.refresh_list()
            else:
                self.info_label.config(text="Title and content cannot be empty.", fg="red")
        else:
            self.info_label.config(text="Please select a note first.", fg="yellow")

    def delete(self):
        if self.selected_id is not None:
            confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this note?")
            if confirm:
                self.cursor.execute("DELETE FROM notes WHERE id=?", (self.selected_id,))
                self.conn.commit()
                self.info_label.config(text="Note deleted.")

                self.title_entry.delete(0, tk.END)
                self.content_text.delete("1.0", tk.END)
                self.refresh_list()
                del self.selected_id
        else:
            self.info_label.config(text="Please select a note first.", fg="yellow")

note_saver = NoteSaver()
