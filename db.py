import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "kavian.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row   # rows behave like dicts: row["email"]
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
