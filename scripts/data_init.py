import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app, db
from app.models import User

with create_app().app_context():
    db.create_all()

    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin', email='admin@example.com', password_hash='hashed_password', role='admin')
        db.session.add(admin_user)
        db.session.commit()
        print("Initial data added.")
