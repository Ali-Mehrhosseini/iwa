import sqlite3

def get_connection():
    conn = sqlite3.connect("kavian.db")
    conn.row_factory = sqlite3.Row   # rows behave like dicts: row["email"]
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn