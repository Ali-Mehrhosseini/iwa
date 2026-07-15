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

**PythonAnywhere URL:** [https://alimehrhosseini.pythonanywhere.com](https://alimehrhosseini.pythonanywhere.com/)

---

## Simulated Current Day and Time

The application uses a **simulated current day and time** within the fictional week (Monday–Sunday).

```
Simulated time: Wednesday 12:00
```

This is set by `SIMULATED_NOW_MINUTE` in `app.py`:

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
| Monday    | 15:00 | The Trial of Alborz     | Pasargad Gate   |
| Tuesday   | 09:00 | The Feather of Simurgh  | Anahita Garden  |
| Tuesday   | 14:00 | The Flame of Azar       | Azar Temple     |
| Wednesday | 14:00 | The Chain of Zahhak     | Azar Temple     |
| Wednesday | 16:30 | Spear of Rostam         | Anahita Garden  |
| Thursday  | 10:00 | The Trial of Alborz     | Azar Temple     |
| Thursday  | 10:00 | The Flame of Azar       | Anahita Garden  |
| Friday    | 10:00 | The Gate of Pasargad    | Anahita Garden  |
| Friday    | 16:00 | Spear of Rostam         | Azar Temple     |
| Saturday  | 11:00 | The Feather of Simurgh  | Anahita Garden  |
| Saturday  | 17:00 | The Chain of Zahhak     | Azar Temple     |
| Sunday    | 12:00 | The Gate of Pasargad    | Pasargad Gate   |
| Sunday    | 16:00 | The Flame of Azar       | Azar Temple     |

### Existing Participations

All three party roles have reservations:

| Adventurer | Quest                   | Day       | Time  | Location        | Role    | Places |
|------------|-------------------------|-----------|-------|-----------------|---------|--------|
| Saghar     | The Feather of Simurgh  | Tuesday   | 09:00 | Anahita Garden  | Healer  | 1      |
| Hossein    | The Flame of Azar       | Tuesday   | 14:00 | Azar Temple     | Warrior | 1      |
| Saghar     | The Flame of Azar       | Tuesday   | 14:00 | Azar Temple     | Mage    | 2      |
| Ali        | The Chain of Zahhak     | Wednesday | 14:00 | Azar Temple     | Warrior | 1      |
| Arya       | The Chain of Zahhak     | Wednesday | 14:00 | Azar Temple     | Warrior | 1      |
| Hossein    | Spear of Rostam         | Wednesday | 16:30 | Anahita Garden  | Warrior | 1      |
| Kian       | The Flame of Azar       | Thursday  | 10:00 | Anahita Garden  | Healer  | 2      |
| Mina       | Spear of Rostam         | Friday    | 16:00 | Azar Temple     | Warrior | 1      |
| Sara       | Spear of Rostam         | Friday    | 16:00 | Azar Temple     | Mage    | 2      |
| Saghar     | The Flame of Azar       | Sunday    | 16:00 | Azar Temple     | Warrior | 2      |

### Testing Scenarios

- **Locked participations (not modifiable):** Log in as Saghar to see her Tuesday 09:00 and 14:00 participations, or as Hossein to see his Tuesday 14:00 and Wednesday 16:30 participations. These sessions start on or before Wednesday 20:00.
- **Modifiable participations:** Saghar's Sunday 16:00 participation is modifiable. Kian's Thursday 10:00 participation and Sara's and Mina's Friday 16:00 participations are also modifiable.
- **Fully booked role:** The Healer role in Thursday's 10:00 Flame of Azar session at Anahita Garden is fully booked (2 of 2 places).
- **Sessions with no participants:** Monday 10:00 and 15:00, Thursday 10:00 at Azar Temple, Friday 10:00, Saturday 11:00 and 17:00, and Sunday 12:00 have no participants and are available for joining.

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
