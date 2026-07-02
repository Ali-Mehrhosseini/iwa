from os import name
from urllib import request  

from flask import Flask, render_template, request

from werkzeug.utils import secure_filename
import uuid


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    list_of_items = ['Email', 'Phone', 'Address']
    return render_template('about.html', items=list_of_items)


application = [
{
    "id": 1,
    "name": "Instagram",
    "subject": "social media",
    "description": "Instagram is a popular social media platform."
},
{
    "id": 2,
    "name": "Google Drive",
    "subject": "cloud storage",
    "description": "Google Drive is a cloud storage service."

},
{
    "id": 3,
    "name": "windows",
    "subject": "operating system",
    "description": "Windows is a popular operating system."
    }




]

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
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        profile_img = request.files.get('profile_img')
        if password != confirm_password:
            return "Passwords do not match", 400
        if profile_img:
            filename = secure_filename(profile_img.filename)
            profile_img.save(f"static/uploads/{filename}")

        
    return render_template('register.html')