from flask import Flask, flash, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import quests_dao
import quest_sessions_dao
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import users_dao
import os

app = Flask(__name__)
app.secret_key = 'sk_live_EjtAS4MInrYlCX0sXD9t55jsLDBx9OQk'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

QUEST_TYPES = ['Razm', 'Rah', 'Chistan', 'Sayeh', 'Atar', 'Alborz']
DIFFICULTIES = ['easy', 'medium', 'hard']

DIFFICULTY_LABELS = {
    'easy':   'Novice — Easy',
    'medium': 'Asha — Medium',
    'hard':   'Kavian — Hard',
}

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
LOCATIONS = ['Azar Temple', 'Anahita Garden', 'Pasargad Gate']


def to_start_minute(day, start_time):
    if day not in DAYS:
        return None
    try:
        hours, minutes = start_time.split(':')
        hours, minutes = int(hours), int(minutes)
    except (ValueError, AttributeError):
        return None
    if not (0 <= hours <= 23 and 0 <= minutes <= 59):
        return None
    return DAYS.index(day) * 1440 + hours * 60 + minutes


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return users_dao.get_user_by_id(int(user_id))


application = [
    {
        "id": 1,
        "name": "John",
        "subject": "Mathematics",
        "description": "Expert in algebra and calculus."
    },
    {
        "id": 2,
        "name": "Sarah",
        "subject": "English",
        "description": "Specialized in literature and writing."
    },
    {
        "id": 3,
        "name": "Mike",
        "subject": "Physics",
        "description": "Physics expert with 10 years experience."
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    list_of_items = ['Email', 'Phone', 'Address']
    return render_template('about.html', items=list_of_items)

@app.route('/tutors')
def find_tutor():
    return render_template('find_tutor.html', application_list=application)


@app.route('/tutors/<int:tutor_id>')
def tutor_detail(tutor_id):
    tutor = next((tutor for tutor in application if tutor["id"] == tutor_id), None)
    if tutor:
        return render_template('tutor_detail.html', tutor=tutor)
    else:
        return "Tutor not found", 404
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        profile_img = request.files.get('profile_img')

        user = users_dao.get_user_by_email(email)
        stored_password_hash = users_dao.get_password_hash(email)

        if user is None or not check_password_hash(stored_password_hash, password):
            return render_template('login.html', error="Invalid email or password")
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name             = request.form.get('name', '').strip()
        email            = request.form.get('email', '').strip()
        password         = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        profile_img      = request.files.get('profile_img')

        # Check 1: nothing empty
        if not name or not email or not password:
            return render_template('register.html', error='All fields are required.')
        # Check 2: password long enough
        if len(password) < 8:
            return render_template('register.html', error='Password must be at least 8 characters.')
        # Check 3: passwords match
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match.')
        # Check 4: email not already used
        if users_dao.get_user_by_email(email) is not None:
            return render_template('register.html', error='That email is already registered.')

        # optional profile image
        img_filename = None
        if profile_img and profile_img.filename != '':
            img_filename = secure_filename(profile_img.filename)
            profile_img.save(os.path.join('static/uploads', img_filename))

        # THE missing piece: actually create the user
        users_dao.create_user(email, generate_password_hash(password),
                              'adventurer', name, img_filename)

        return redirect(url_for('login'))          # success → go log in

    return render_template('register.html')        # the GET case


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/quests")
@login_required
def quests():
    all_quests = quests_dao.get_all_quests()
    return render_template("quests.html", quests=all_quests, difficulty_labels=DIFFICULTY_LABELS)


@app.route("/quests/new", methods=['GET', 'POST'])
@login_required
def new_quest():
    if not current_user.is_guild_master():
        flash("Access denied. Only guild masters can create new quests.", "error")
        return redirect(url_for('home'))
    if request.method == 'POST':
        title = request.form.get('title')
        duration_minutes = request.form.get('duration_minutes')
        quest_type = request.form.get('quest_type')
        difficulty = request.form.get('difficulty')
        description = request.form.get('description')
        image = request.files.get('image')

        # Handle image upload
        image_filename = None
        if image and image.filename != '':
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        # Save the new quest to the database
        quests_dao.create_quest(title, duration_minutes, quest_type, difficulty, description, image_filename)
        flash("New quest created successfully!", "success")
        return redirect(url_for('quests'))

    return render_template("new_quest.html", quest_types=QUEST_TYPES, difficulties=DIFFICULTIES, difficulty_labels=DIFFICULTY_LABELS)


@app.route('/sessions/new', methods=['GET', 'POST'])
@login_required
def new_session():
    if not current_user.is_guild_master():
        flash('Only the Guild Master can schedule sessions')
        return redirect(url_for('home'))

    if request.method == 'POST':
        quest_id = request.form.get('quest_id')
        day = request.form.get('day')
        start_time = request.form.get('start_time')
        location = request.form.get('location')

        errors = []

        quest = None
        if quest_id and quest_id.isdigit():
            quest = quests_dao.get_quest_by_id(int(quest_id))
        if quest is None:
            errors.append('Unknown quest')

        if location not in LOCATIONS:
            errors.append('Invalid location')

        start_minute = to_start_minute(day, start_time)
        if start_minute is None:
            errors.append('Invalid day or time')

        if not errors:
            end_minute = start_minute + quest.duration_minutes
            if quest_sessions_dao.has_location_conflict(location, start_minute, end_minute):
                errors.append(f'{location} is already booked at that time')

        if errors:
            for error in errors:
                flash(error)
            return redirect(url_for('new_session'))

        quest_sessions_dao.create_session(quest.id, day, start_time,
                                          start_minute, location)
        flash('Session scheduled')
        return redirect(url_for('home'))

    return render_template('new_session.html',
                           quests=quests_dao.get_all_quests(),
                           days=DAYS,
                           locations=LOCATIONS)
