from db import get_connection
from models import User

def get_user_by_email(email):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    if row is None:
        return None
    return User(row["id"], row["email"], row["role"], row["display_name"], row["profile_img"])

def get_user_by_id(user_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if row is None:
        return None
    return User(row["id"], row["email"], row["role"], row["display_name"], row["profile_img"])

def get_password_hash(email):
    conn = get_connection()
    row = conn.execute("SELECT password_hash FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return row["password_hash"] if row else None

def create_user(email, password_hash, role, display_name, profile_img):
    conn = get_connection()
    conn.execute(
        "INSERT INTO users (email, password_hash, role, display_name, profile_img) VALUES (?, ?, ?, ?, ?)",
        (email, password_hash, role, display_name, profile_img),
    )
    conn.commit()
    conn.close()