import unittest
from app import create_app, db
from app.models import User

class LibraryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        response = self.app.test_client().post('/register', data=dict(
            username='testuser',
            email='test@example.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created!', response.data)

    def test_login_user(self):
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        response = self.app.test_client().post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)
