import unittest
import json
from src.database import db
from src import create_app


class AuthTestCase(unittest.TestCase):
    """Test case for the authentication blueprint."""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app()
        self.client = self.app.test_client
        self.user_data = {
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'password': 'test_password'
        }

        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_registration(self):
        """Test user registration works correcty."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        result = json.loads(res.data.decode())
        self.assertEqual(
            result['message'], "Customer created")
        self.assertEqual(res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 409)
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['error'], "Email already be assigned to another user.")

    def test_user_login(self):
        """Test registered user can login."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data)
        result = json.loads(login_res.data.decode())
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access'])

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        not_a_user = {
            'email': 'not_a_user@example.com',
            'password': 'nope'
        }
        res = self.client().post('/auth/login', data=not_a_user)
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            result['error'], "Wrong credentials")