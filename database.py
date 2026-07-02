import sqlite3


conn = sqlite3.connect('database.db')
cursor = conn.cursor()

sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            surname TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            profile_img TEXT    
                        );'''

cursor.execute(sqlite_create_table_query)
conn.commit()