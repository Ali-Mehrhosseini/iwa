# Kavian Guild — Fantasy Adventure Guild Manager

**Introduction to Web Applications — Exam Session 16/07/2026**  
**Author:** Ali Mehrhosseini

---

## Project Description

Kavian Guild is a web application for managing a fantasy adventure guild's weekly quest program. Inspired by ancient Persian mythology, the guild offers quests across three legendary locations: **Azar Temple**, **Anahita Garden**, and **Pasargad Gate**.

The application supports two user roles:

- **Adventurers** can browse quests, join quest sessions (choosing a party role: Warrior, Mage, or Healer), and manage their reservations.
- **Guild Master (Darius)** can create new quests, schedule quest sessions, and view guild statistics from the dashboard.

Unregistered users can freely explore the quest board and quest details.

### Target Device

Desktop (responsive layout via Bootstrap).

---

## Deployed Application

**PythonAnywhere URL:** `https://YOUR_USERNAME.pythonanywhere.com`

*(Replace with actual URL after deployment.)*

---

## Simulated Current Day and Time

The application uses a **simulated current day and time** within the fictional week (Monday–Sunday).

```
Simulated time: Wednesday 12:00
```

This is set in `app.py` at line 52:

```python
SIMULATED_NOW_MINUTE = 3600   # Wednesday 12:00 → 2×1440 + 12×60
```

### Effect on Participations

- Quest sessions starting **on or before Wednesday 20:00** are locked — participations **cannot** be modified or cancelled.
- Quest sessions starting **after Wednesday 20:00** are still modifiable.

---

## User Credentials

All accounts use the password: **`test1234`**

### Guild Master

| Role         | Email             | Password   | Display Name |
|-------------|-------------------|------------|-------------|
| Guild Master | darius@guild.com  | test1234   | Darius      |

### Adventurers

| Email                        | Password   | Display Name |
|-----------------------------|------------|-------------|
| arya@example.com            | test1234   | Arya        |
| sara@example.com            | test1234   | Sara        |
| kian@example.com            | test1234   | Kian        |
| mina@example.com            | test1234   | Mina        |
| ali_mehrhosseini@yhoo.com   | test1234   | Ali         |
| saghar@gmail.com            | test1234   | Saghar      |
| hossein@gmail.com           | test1234   | Hossein     |

---

## Sample Data Overview

### Quests (6)

| Quest                    | Type    | Difficulty | Duration |
|-------------------------|---------|------------|----------|
| Spear of Rostam         | Razm    | Medium     | 90 min   |
| The Trial of Alborz     | Alborz  | Hard       | 150 min  |
| The Chain of Zahhak     | Sayeh   | Medium     | 120 min  |
| The Gate of Pasargad    | Chistan | Easy       | 60 min   |
| The Feather of Simurgh  | Rah     | Hard       | 180 min  |
| The Flame of Azar       | Atar    | Medium     | 90 min   |

### Quest Sessions (14 sessions across all 7 days)

| Day       | Time  | Quest                   | Location        |
|-----------|-------|-------------------------|-----------------|
| Monday    | 10:00 | The Gate of Pasargad    | Pasargad Gate   |
| Monday    | 15:00 | The Trial of Alborz     | Anahita Garden  |
| Tuesday   | 09:00 | The Feather of Simurgh  | Anahita Garden  |
| Tuesday   | 14:00 | The Flame of Azar       | Azar Temple     |
| Wednesday | 14:00 | The Chain of Zahhak     | Azar Temple     |
| Wednesday | 16:30 | Spear of Rostam         | Anahita Garden  |
| Thursday  | 10:00 | The Trial of Alborz     | Azar Temple     |
| Thursday  | 10:00 | The Flame of Azar       | Anahita Garden  |
| Thursday  | 17:00 | The Trial of Alborz     | Pasargad Gate   |
| Friday    | 16:00 | Spear of Rostam         | Azar Temple     |
| Saturday  | 11:00 | The Feather of Simurgh  | Anahita Garden  |
| Saturday  | 17:00 | The Chain of Zahhak     | Azar Temple     |
| Sunday    | 12:00 | The Gate of Pasargad    | Pasargad Gate   |
| Sunday    | 16:00 | The Flame of Azar       | Azar Temple     |

### Existing Participations

All three party roles have reservations:

| Adventurer | Quest                  | Role    | Places |
|-----------|------------------------|---------|--------|
| Ali       | The Chain of Zahhak    | Warrior | 1      |
| Arya      | The Chain of Zahhak    | Warrior | 1      |
| Sara      | Spear of Rostam        | Mage    | 2      |
| Kian      | The Flame of Azar      | Healer  | 2      |
| Mina      | Spear of Rostam        | Warrior | 1      |
| Saghar    | The Feather of Simurgh | Healer  | 1      |
| Saghar    | The Flame of Azar      | Mage    | 2      |
| Saghar    | The Gate of Pasargad   | Mage    | 1      |
| Hossein   | The Flame of Azar      | Warrior | 1      |
| Hossein   | Spear of Rostam        | Warrior | 1      |

### Testing Scenarios

- **Locked participations (not modifiable):** Log in as Saghar or Hossein — their Tuesday participations are locked because those sessions are before Wednesday 20:00.
- **Modifiable participations:** Log in as Sara, Kian, or Mina — their Thursday/Friday participations can still be modified or cancelled.
- **Sessions with no participants:** Sessions on Monday, Thursday (10:00 Azar Temple), Thursday (17:00), Saturday, and Sunday (16:00) have no participants and are available for joining.

---

## Technologies Used

- **Backend:** Flask 3.1.1, Flask-Login 0.6.3
- **Database:** SQLite (file: `kavian.db`)
- **Frontend:** HTML5, CSS3, Bootstrap 5.3.8
- **Authentication:** Flask-Login with Werkzeug password hashing

---

## How to Run Locally

1. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # macOS / Linux
   venv\Scripts\activate           # Windows
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   flask run
   ```

4. **Open in browser:**

   ```
   http://127.0.0.1:5000
   ```

---

## Project Structure

```
iwa/
├── app.py                  # Main Flask application and routes
├── db.py                   # Database connection helper
├── models.py               # User, Quest, QuestSession, Participation models
├── users_dao.py            # Data access for users
├── quests_dao.py           # Data access for quests
├── quest_sessions_dao.py   # Data access for quest sessions
├── participations_dao.py   # Data access for participations
├── schema.sql              # Database schema definition
├── kavian.db               # SQLite database with sample data
├── requirements.txt        # Python dependencies
├── static/
│   ├── style.css           # Custom CSS styles
│   ├── main.js             # Client-side JavaScript
│   ├── images/             # Static images (logo, backgrounds)
│   └── uploads/            # Uploaded quest images
└── templates/
    ├── base.html           # Base layout template
    ├── index.html          # Homepage with quest board and filters
    ├── login.html          # Login page
    ├── register.html       # Registration page
    ├── quests.html         # Quest catalog
    ├── quest_detail.html   # Individual quest with linked sessions
    ├── new_quest.html      # Create quest form (Guild Master)
    ├── new_session.html    # Schedule session form (Guild Master)
    ├── session_detail.html # Session details with join form
    ├── my_scroll.html      # Adventurer reservations page
    └── guild_dashboard.html # Guild Master dashboard
```
