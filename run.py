from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Import Migrate

db = SQLAlchemy()  # Initialize SQLAlchemy
migrate = Migrate()  # Initialize Migrate

def create_app():
    app = Flask(__name__)

    # Set the database URI (ensure it's correct)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Initialize the database with app
    migrate.init_app(app, db)  # Initialize Flask-Migrate with app and db

    # Import and register blueprints, routes, etc.
    with app.app_context():
        # Include other app-specific initializations, e.g. routes, models, etc.
        pass

    return app

from app import create_app

# Create the Flask app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
