from db import get_connection
from models import Quest

def get_all_quests():
    conn = get_connection()
    rows = conn.execute("""
        SELECT id, title, duration_minutes, quest_type, difficulty, description, image FROM quests """).fetchall()
    conn.close()
    return [
        Quest(
            row["id"],
            row["title"],
            row["duration_minutes"],
            row["quest_type"],
            row["difficulty"],
            row["description"],
            row["image"],
        )
        for row in rows
    ]

def create_quest(title, duration_minutes, quest_type, difficulty, description, image):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO quests (title, duration_minutes, quest_type, difficulty, description, image)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, duration_minutes, quest_type, difficulty, description, image),
    )
    conn.commit()
    conn.close()

def get_quest_by_id(quest_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM quests WHERE id = ?", (quest_id,)
    ).fetchone()
    conn.close()
    if row is None:
        return None
    return Quest(
        row["id"],
        row["title"],
        row["duration_minutes"],
        row["quest_type"],
        row["difficulty"],
        row["description"],
        row["image"],
    )