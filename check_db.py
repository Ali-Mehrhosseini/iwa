import sqlite3

conn = sqlite3.connect('kavian.db')
conn.row_factory = sqlite3.Row

print('=== USERS ===')
for r in conn.execute('SELECT id, email, role, display_name FROM users'):
    print(dict(r))

print('\n=== QUESTS ===')
for r in conn.execute('SELECT id, title, quest_type, difficulty, duration_minutes, image FROM quests'):
    print(dict(r))

print('\n=== SESSIONS ===')
for r in conn.execute('SELECT s.id, s.day, s.start_time, s.start_minute, s.location, q.title FROM quest_sessions s JOIN quests q ON s.quest_id = q.id ORDER BY s.start_minute'):
    print(dict(r))

print('\n=== PARTICIPATIONS ===')
for r in conn.execute('SELECT p.id, u.display_name, u.email, q.title, p.role, p.places, s.day, s.start_time, s.start_minute FROM participations p JOIN users u ON p.user_id = u.id JOIN quest_sessions s ON p.session_id = s.id JOIN quests q ON s.quest_id = q.id'):
    print(dict(r))

# Check role counts per session
print('\n=== ROLE TOTALS BY SESSION ===')
for r in conn.execute('''
    SELECT s.id, q.title, s.day, s.start_time, p.role, SUM(p.places) as total
    FROM participations p
    JOIN quest_sessions s ON p.session_id = s.id
    JOIN quests q ON s.quest_id = q.id
    GROUP BY s.id, p.role
    ORDER BY s.start_minute, p.role
'''):
    print(dict(r))

conn.close()
