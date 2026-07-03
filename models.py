from flask_login import UserMixin

class User(UserMixin):                      # UserMixin = Flask-Login support
    def __init__(self, id, email, role, display_name, profile_img=None):
        self.id = id
        self.email = email
        self.role = role
        self.display_name = display_name
        self.profile_img = profile_img  # Initialize profile_img attribute

    def is_guild_master(self):              # handy helper for permission checks
        return self.role == "guildmaster"

class Quest:
    def __init__(self, id, title, duration_minutes, quest_type, difficulty, description, image):
        self.id = id
        self.title = title
        self.duration_minutes = duration_minutes
        self.quest_type = quest_type
        self.difficulty = difficulty
        self.description = description
        self.image = image

class QuestSession:
    def __init__(self, id, quest_id, day, start_time, start_minute, location):
        self.id = id
        self.quest_id = quest_id
        self.day = day
        self.start_time = start_time
        self.start_minute = start_minute
        self.location = location

class Participation:
    def __init__(self, id, user_id, session_id, role, places):
        self.id = id
        self.user_id = user_id
        self.session_id = session_id
        self.role = role
        self.places = places