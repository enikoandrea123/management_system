from flask import Blueprint, render_template, redirect, url_for, flash, request, Flask
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from app import db
from app.models import User, Book, BorrowHistory
from app.forms import LoginForm, RegistrationForm  # This import should now work
from datetime import datetime

app = Flask(__name__)
# Define the Blueprint
main_bp = Blueprint('main', __name__)
login_manager = LoginManager()
login_manager.init_app(app)

@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))

    return render_template('login.html', form=form)


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role='student')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.dashboard'))
    return render_template('register.html', form=form)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    borrowed_books = BorrowHistory.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', borrowed_books=borrowed_books)


@main_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@login_manager.user_loader
def load_user(user_id):
    # Assuming you are using an ORM like SQLAlchemy
    # You should replace this with your actual query logic to find the user by ID
    return User.query.get(int(user_id))  # Replace with how you retrieve a user in your DB