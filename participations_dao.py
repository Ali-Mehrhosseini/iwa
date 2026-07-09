from db import get_connection


def get_role_totals(session_id, exclude_participation_id=None):
    conn = get_connection()

    sql = """
        SELECT role, COALESCE(SUM(places), 0) AS places
        FROM participations
        WHERE session_id = ?
    """
    params = [session_id]

    if exclude_participation_id is not None:
        sql += " AND id != ?"
        params.append(exclude_participation_id)

    sql += " GROUP BY role"

    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return {row["role"]: row["places"] for row in rows}


def get_user_participation(session_id, user_id):
    conn = get_connection()
    row = conn.execute(
        """
        SELECT id, user_id, session_id, role, places
        FROM participations
        WHERE session_id = ? AND user_id = ?
        """,
        (session_id, user_id),
    ).fetchone()
    conn.close()
    return row


def get_participation_by_id(participation_id):
    conn = get_connection()
    row = conn.execute(
        """
        SELECT p.id, p.user_id, p.session_id, p.role, p.places,
               s.start_minute
        FROM participations p
        JOIN quest_sessions s ON p.session_id = s.id
        WHERE p.id = ?
        """,
        (participation_id,),
    ).fetchone()
    conn.close()
    return row

def count_user_sessions(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT COUNT(DISTINCT session_id) AS session_count FROM participations WHERE user_id = ?',
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row['session_count']


def create_participation(user_id, session_id, role, places):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO participations (user_id, session_id, role, places)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, session_id, role, places),
    )
    conn.commit()
    conn.close()



def has_time_overlap(user_id, new_start, new_end):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) AS clash_count
        FROM participations p
        JOIN quest_sessions s ON p.session_id = s.id
        JOIN quests q ON s.quest_id = q.id
        WHERE p.user_id = ?
          AND s.start_minute < ?
          AND ? < s.start_minute + q.duration_minutes
    ''', (user_id, new_end, new_start))
    row = cursor.fetchone()
    conn.close()
    return row['clash_count'] > 0


def get_user_places_for_role(user_id, session_id, role):
    conn = get_connection()
    row = conn.execute(
        'SELECT COALESCE(SUM(places), 0) AS places FROM participations WHERE user_id = ? AND session_id = ? AND role = ?',
        (user_id, session_id, role),
    ).fetchone()
    conn.close()
    return row['places']


def update_participation(participation_id, role, places):
    conn = get_connection()
    conn.execute(
        'UPDATE participations SET role = ?, places = ? WHERE id = ?',
        (role, places, participation_id),
    )
    conn.commit()
    conn.close()


def delete_participation(participation_id):
    conn = get_connection()
    conn.execute(
        'DELETE FROM participations WHERE id = ?',
        (participation_id,),
    )
    conn.commit()
    conn.close()

def get_user_participations(user_id):
    conn = get_connection()
    rows = conn.execute(
        '''
        SELECT p.id, p.role, p.places,
               s.id AS session_id, s.day, s.start_time, s.start_minute, s.location,
               q.title AS quest_title
        FROM participations p
        JOIN quest_sessions s ON p.session_id = s.id
        JOIN quests q ON s.quest_id = q.id
        WHERE p.user_id = ?
        ORDER BY s.start_minute
        ''',
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def get_guild_stats():
    conn = get_connection()
    cursor = conn.cursor()

    quest_count = cursor.execute(
        'SELECT COUNT(*) AS n FROM quests'
    ).fetchone()['n']

    session_count = cursor.execute(
        'SELECT COUNT(*) AS n FROM quest_sessions'
    ).fetchone()['n']

    total_places = cursor.execute(
        'SELECT COALESCE(SUM(places), 0) AS n FROM participations'
    ).fetchone()['n']

    conn.close()
    return {
        'quest_count': quest_count,
        'session_count': session_count,
        'total_places': total_places,
    }

def session_has_participations(session_id):
    conn = get_connection()
    row = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM participations
        WHERE session_id = ?
        """,
        (session_id,),
    ).fetchone()
    conn.close()

    return row["count"] > 0