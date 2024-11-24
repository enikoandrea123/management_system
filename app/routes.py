from flask import Blueprint, render_template, redirect, url_for, flash, request, Flask
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from app.models import BorrowHistory
from app.forms import LoginForm, RegisterForm
from flask import render_template, redirect, url_for, flash
from app import db
from app.models import User
from werkzeug.security import generate_password_hash

app = Flask(__name__)

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
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', 'error')
            return redirect(url_for('main.register'))

        user_email = User.query.filter_by(email=email).first()
        if user_email:
            flash('Email already registered', 'error')
            return redirect(url_for('main.register'))

        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return redirect(url_for('main.register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password, role='student')
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('main.login'))

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
    return User.query.get(int(user_id))
