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