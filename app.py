from flask import Flask, flash, request, render_template, redirect, url_for, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import quests_dao
import quest_sessions_dao
import participations_dao
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import users_dao
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-me')
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

ROLE_CAPACITIES = {'Warrior': 4, 'Mage': 3, 'Healer': 2}


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


SIMULATED_NOW_MINUTE = 3600   # Wednesday 12:00  →  2*1440 + 12*60
LOCK_WINDOW_MINUTES = 480     # 8 hours * 60

def is_locked(start_minute):
    """A booking for this session can no longer be modified or cancelled."""
    return start_minute <= SIMULATED_NOW_MINUTE + LOCK_WINDOW_MINUTES


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
    sessions = quest_sessions_dao.get_week_program()
    return render_template('index.html', sessions=sessions, difficulty_labels=DIFFICULTY_LABELS)

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
            flash('Invalid email or password', 'danger')
            return render_template('login.html', error="Invalid email or password")
        else:
            login_user(user)
            flash('Login successful!', 'success')
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
    flash('You have been logged out.', 'success')
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


@app.route('/sessions/<int:session_id>')
def session_detail(session_id):
    session_row = quest_sessions_dao.get_session_by_id(session_id)
    if session_row is None:
        abort(404)
    role_totals = participations_dao.get_role_totals(session_id)
    user_participation = None
    if current_user.is_authenticated:
        user_participation = participations_dao.get_user_participation(session_id, current_user.id)
    return render_template(
        'session_detail.html',
        s=session_row,
        difficulty_labels=DIFFICULTY_LABELS,
        role_capacities=ROLE_CAPACITIES,
        role_totals=role_totals,
        user_participation=user_participation,
    )


@app.route('/sessions/<int:session_id>/join', methods=['POST'])
@login_required
def join_session(session_id):
    session_row = quest_sessions_dao.get_session_by_id(session_id)
    if session_row is None:
        abort(404)

    if current_user.is_guild_master():
        flash('The Guild Master cannot join quest sessions.')
        return redirect(url_for('session_detail', session_id=session_id))

    role = request.form.get('role')
    places_raw = request.form.get('places')

    if role not in ROLE_CAPACITIES:
        flash('Invalid party role.')
        return redirect(url_for('session_detail', session_id=session_id))

    try:
        places = int(places_raw)
    except (TypeError, ValueError):
        places = 0

    if places not in (1, 2):
        flash('Reserved places must be 1 or 2.')
        return redirect(url_for('session_detail', session_id=session_id))

    new_start = session_row['start_minute']
    new_end = new_start + session_row['duration_minutes']

    if participations_dao.has_time_overlap(current_user.id, new_start, new_end):
        flash('This session overlaps with a quest you have already joined.', 'danger')
        return redirect(url_for('session_detail', session_id=session_id))

    if participations_dao.get_user_participation(session_id, current_user.id):
        flash('You have already joined this session.')
        return redirect(url_for('session_detail', session_id=session_id))

    role_totals = participations_dao.get_role_totals(session_id)
    reserved = role_totals.get(role, 0)
    capacity = ROLE_CAPACITIES[role]
    if reserved + places > capacity:
        flash(f'Not enough {role} places remain.')
        return redirect(url_for('session_detail', session_id=session_id))
    
    if participations_dao.count_user_sessions(current_user.id) >= 3:
        flash('You have already joined 3 quest sessions this week — the maximum allowed.', 'danger')
        return redirect(url_for('session_detail', session_id=session_id))

    # WALL 4 — max 2 places per role per user
    mine = participations_dao.get_user_places_for_role(current_user.id, session_id, role)
    if mine + places > 2:
        flash('You cannot hold more than 2 places for the same role in this session.', 'danger')
        return redirect(url_for('session_detail', session_id=session_id))
    
    participations_dao.create_participation(current_user.id, session_id, role, places)
    flash('You joined the quest session.')
    return redirect(url_for('session_detail', session_id=session_id))


@app.route('/participations/<int:participation_id>/modify', methods=['POST'])
@login_required
def modify_participation(participation_id):
    # 1. Fetch (gives us user_id + start_minute + session_id)
    participation = participations_dao.get_participation_by_id(participation_id)
    if not participation:
        abort(404)

    # 2. Ownership
    if participation['user_id'] != current_user.id:
        abort(403)

    # 3. 8-hour lock
    if is_locked(participation['start_minute']):
        flash('This booking can no longer be modified (starts within 8 hours).', 'danger')
        return redirect(url_for('my_scroll'))

    # 4. Validate the NEW form values
    role = request.form.get('role')
    places = request.form.get('places')
    if role not in ROLE_CAPACITIES:
        flash('Invalid role.', 'danger')
        return redirect(url_for('my_scroll'))
    if places not in ('1', '2'):
        flash('Invalid number of places.', 'danger')
        return redirect(url_for('my_scroll'))
    places = int(places)

    # 5. Wall 3 re-run — role capacity, EXCLUDING this booking so we don't fight ourselves
    session_id = participation['session_id']
    taken_by_others = participations_dao.get_role_totals(
        session_id, exclude_participation_id=participation_id
    ).get(role, 0)
    if taken_by_others + places > ROLE_CAPACITIES[role]:
        flash(f'Not enough {role} places left in this session.', 'danger')
        return redirect(url_for('my_scroll'))

    # 6. Save, confirm, redirect
    participations_dao.update_participation(participation_id, role, places)
    flash('Your booking has been updated.', 'success')
    return redirect(url_for('my_scroll'))


@app.route('/participations/<int:participation_id>/cancel', methods=['POST'])
@login_required
def cancel_participation(participation_id):
    participation = participations_dao.get_participation_by_id(participation_id)
    if not participation:
        abort(404)

    if participation['user_id'] != current_user.id:
        abort(403)

    if is_locked(participation['start_minute']):
        flash('This booking can no longer be cancelled (starts within 8 hours).', 'danger')
        return redirect(url_for('my_scroll'))

    participations_dao.delete_participation(participation_id)
    flash('Your booking has been cancelled.', 'success')
    return redirect(url_for('my_scroll'))


@app.route('/my-reservations')
@login_required
def my_scroll():
    participations = participations_dao.get_user_participations(current_user.id)
    return render_template('my_scroll.html', participations=participations, is_locked=is_locked)


@app.route('/guild-dashboard')
@login_required
def guild_dashboard():
    if not current_user.is_guild_master():
        abort(403)

    stats = participations_dao.get_guild_stats()
    return render_template('guild_dashboard.html', stats=stats)
