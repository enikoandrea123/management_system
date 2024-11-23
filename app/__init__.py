from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Define db and login_manager at the top but don't import them here yet
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Load configuration

    db.init_app(app)  # Initialize the database
    login_manager.init_app(app)  # Initialize Flask-Login
    login_manager.login_view = 'main.login'  # Set the login view

    # Import models and routes inside the function to avoid circular imports
    from app.models import User  # Import here to avoid circular import
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Query for the user by ID

    return app
