# SQLite Note Saver 

A simple desktop GUI application built with **Python**, **Tkinter**, and **SQLite** for creating, viewing, updating, and deleting notes.

---

## Features

- Add new notes
- View and select saved notes
- Edit and update selected notes
- Delete notes with confirmation
- Notes are stored in a local `SQLite` database file (`notes.db`)
- Desktop GUI built with `Tkinter` and `grid()` layout system

---

## Interface

| Component         | Description                             |
|------------------|-----------------------------------------|
| `Title` entry     | Title of the note                       |
| `Content` text    | Body/content of the note                |
| `Save` button     | Saves a new note to the database        |
| `Update` button   | Updates the selected note               |
| `Delete` button   | Deletes the selected note after prompt  |
| `Listbox`         | Displays titles of all saved notes      |
| `Label`           | Provides dynamic feedback to the user   |

---

## Getting Started

### Requirements
- Python 3.x

> No external packages required — uses built-in `tkinter` and `sqlite3` modules.

### Run the App

```bash
python note_saver.py