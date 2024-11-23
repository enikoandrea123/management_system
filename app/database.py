from app import db
from app import create_app

app = create_app()

with app.app_context():
    db.create_all()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # This creates the necessary tables for your models
