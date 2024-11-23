import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_random_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///library.db'
    SESSION_PROTECTION = 'strong'
    LOGIN_DISABLED = False
