import sqlite3
import time

class db_handle:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.setup_db()

    def setup_db(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )"""
        self.cursor.execute(query)
        self.connection.commit()

    def add_item(self, title):
        query = "INSERT INTO tasks (title, time) VALUES (?, ?)"
        self.cursor.execute(query, (title, str(time.time())))
        self.connection.commit()

    def list_items(self):
        query = "SELECT id, title, time, status FROM tasks"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        print(f"{'ID':<5} {'Title':<20} {'Status':<10}")
        print("-" * 35)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[3]:<10}")

    def update_status(self, task_id, new_status):
        query = "UPDATE tasks SET status = ? WHERE id = ?"
        self.cursor.execute(query, (new_status, task_id))
        self.connection.commit()

        if self.cursor.rowcount == 0:
            print(f"Error: No task found with ID {task_id}")
        else:
            print(f"Task {task_id} updated to '{new_status}'")
    def edit_task(self, task_id, new_name):
        query = "UPDATE tasks SET title = ? WHERE id = ?"
        self.cursor.execute(query, (new_name, task_id))
        self.connection.commit()

        if self.cursor.rowcount == 0:
            print(f"Error: No task found with ID {task_id}")
        else:
            print(f"Task {task_id} updated to '{new_name}'")

    def close(self):
        self.connection.close()

db = db_handle("library.db")

def handle_input(text):
    parsed = text.partition(' ')
    command, sep, name = parsed
    id_in, sep, data = name.partition(' ')
    if command == "add":
        db.add_item(name)
    elif command == "list":
        db.list_items()
    elif command == "update":
        db.update_status(id_in, data)
    elif command == "edit":
        db.edit_task(id_in, data)
    elif command == "exit":
        db.close()
        exit()
while True:
    handle_input(input("Input command: "))
