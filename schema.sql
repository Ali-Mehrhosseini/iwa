PRAGMA foreign_keys = ON;

CREATE TABLE users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT    NOT NULL UNIQUE,
    password_hash TEXT    NOT NULL,
    role          TEXT    NOT NULL CHECK (role IN ('adventurer', 'guildmaster')),
    display_name  TEXT    NOT NULL,
    profile_img   TEXT                      
);

CREATE TABLE quests (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    title            TEXT    NOT NULL,
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
    quest_type       TEXT    NOT NULL CHECK (quest_type IN ('Razm','Rah','Chistan','Sayeh','Atar','Alborz')),
    difficulty       TEXT    NOT NULL CHECK (difficulty IN ('easy','medium','hard')),
    description      TEXT    NOT NULL,
    image            TEXT
);

CREATE TABLE quest_sessions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    quest_id     INTEGER NOT NULL,
    day          TEXT    NOT NULL,
    start_time   TEXT    NOT NULL,
    start_minute INTEGER NOT NULL,
    location     TEXT    NOT NULL CHECK (location IN  ('Azar Temple','Anahita Garden','Pasargad Gate')),
    FOREIGN KEY (quest_id) REFERENCES quests(id)
);

CREATE TABLE participations (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    session_id INTEGER NOT NULL,
    role       TEXT    NOT NULL CHECK (role IN ('Warrior','Mage','Healer')),
    places     INTEGER NOT NULL CHECK (places IN (1, 2)),
    FOREIGN KEY (user_id)    REFERENCES users(id),
    FOREIGN KEY (session_id) REFERENCES quest_sessions(id)
);
