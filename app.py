from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import logging
import os
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Use environment variables for configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Initialize the URLSafeTimedSerializer
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Placeholder data structures
users = [
    {"username": "testuser", "email": "testuser@example.com", "password": bcrypt.generate_password_hash("password").decode('utf-8')}
]
jobs = [
    {"id": 1, "title": "Software Engineer", "description": "Develop software applications."},
    {"id": 2, "title": "Data Analyst", "description": "Analyze data and generate insights."}
]

@login_manager.user_loader
def load_user(user_id):
    return next((user for user in users if user.get('id') == int(user_id)), None)

@app.route('/')
def home():
    return render_template('home.html', jobs=jobs, company_name='Kratos')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users.append({"username": username, "email": email, "password": hashed_password})
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = next((user for user in users if user["email"] == email), None)
        if user and bcrypt.check_password_hash(user["password"], password):
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', debug=True)

