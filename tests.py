from datetime import datetime, timezone, timedelta
import unittest
from app import create_app, db
from app.models import User, Task
from config import Config
import base64
from flask import jsonify


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    


class TasksCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='vasja')
        u.set_password('dkf')
        self.assertFalse(u.check_password('d'))
        self.assertTrue(u.check_password('dkf'))

    def test_access(self):
        response = self.client.get('/tasks')
        assert response.status_code == 401

    def test_create_task(self):
        u = User(username='tuzic')
        u.set_password('1234')
        response = self.client.post(
            '/tokens', 
            headers = {
                "Authorization": 
                "Basic "+ base64.b64encode(
                    "tuzic:1234".encode()).decode('utf-8')
            }
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'token' in data
        token = data['token']
        response = self.client.post(
            '/tasks', 
            headers={"Authorization":f"Bearer {token}"},
            json={"title": "ts1"})
        assert response.status_code == 201
        data = response.get_json()
        assert 'title' in data
        assert data['title'] == 'ts1'

if __name__ == '__main__':
    unittest.main(verbosity=2)