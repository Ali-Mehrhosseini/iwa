from db import get_connection

def has_location_conflict(location, new_start, new_end):
    conn = get_connection()
    row = conn.execute(
        """SELECT COUNT(*) AS conflicts
           FROM quest_sessions s
           JOIN quests q ON s.quest_id = q.id
           WHERE s.location = ?
             AND s.start_minute < ?
             AND ? < s.start_minute + q.duration_minutes""",
        (location, new_end, new_start)
    ).fetchone()
    conn.close()
    return row["conflicts"] > 0


def create_session(quest_id, day, start_time, start_minute, location):
    conn = get_connection()
    conn.execute(
        """INSERT INTO quest_sessions (quest_id, day, start_time, start_minute, location)
           VALUES (?, ?, ?, ?, ?)""",
        (quest_id, day, start_time, start_minute, location),
    )
    conn.commit()
    conn.close()


def get_week_program(day=None, quest_type=None, difficulty=None ,role=None, role_capacity=None):
    query = """SELECT s.id, s.day, s.start_time, s.location,
                      q.title, q.quest_type, q.difficulty, q.duration_minutes, q.image
               FROM quest_sessions s
               JOIN quests q ON s.quest_id = q.id"""
    conditions = []
    params = []
    if day:
        conditions.append("s.day = ?")
        params.append(day)
    if quest_type:
        conditions.append("q.quest_type = ?")
        params.append(quest_type)
    if difficulty:
        conditions.append("q.difficulty = ?")
        params.append(difficulty)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY s.start_minute"

    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows

def get_session_by_id(session_id):
    conn = get_connection()
    row = conn.execute(
        """SELECT s.id, s.day, s.start_time, s.start_minute, s.location,
                  q.title, q.quest_type, q.difficulty, q.duration_minutes,
                  q.description, q.image
           FROM quest_sessions s
           JOIN quests q ON s.quest_id = q.id
           WHERE s.id = ?""",(session_id,)).fetchone()
    conn.close()
    return row

