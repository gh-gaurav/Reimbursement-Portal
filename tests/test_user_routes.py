import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Importing text function
from flask_testing import TestCase
from main import create_app, db
from models import User, Role  # Assuming Role is defined in models.py
from config import TestConfig

class TestUserCreation(TestCase):

    def create_app(self):
        app = create_app()
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        # Handling foreign key constraint error when dropping tables
        try:
            db.drop_all()
        except Exception as e:
            db.session.rollback()
            print("Error while dropping tables:", e)

    def test_create_user(self):
        # Check if the user already exists
        existing_user = User.query.filter_by(username='ravi').first()
        if existing_user:
            print("User 'ravi' already exists, skipping insertion.")
            return

        # Inserting a user directly into the database
        insert_query = text(
            "INSERT INTO users(username, email, role, password_hash, first_name, last_name) VALUES (:username, :email, :role, :password_hash, :first_name, :last_name)"
        )
        db.session.execute(
            insert_query,
            {
                "username": "ravi",
                "email": "ravi@gmail.com",
                "role": "Admin",
                "password_hash": "abcxyz123",
                "first_name": "Ravi",
                "last_name": "Sharma"
            }
        )
        db.session.commit()

        # Retrieving the inserted user from the database
        user = User.query.filter_by(username='ravi').first()

        # Asserting that the user exists in the database
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'ravi')
        self.assertEqual(user.email, 'ravi@gmail.com')
        # Assuming Role.Admin is defined in your Role enumeration
        self.assertEqual(user.role, Role.Admin)
        self.assertEqual(user.password_hash, 'abcxyz123')
        self.assertEqual(user.first_name, 'Ravi')
        self.assertEqual(user.last_name, 'Sharma')

    def test_get_user(self):
        existing_user = User.query.filter_by(username='ravi').first()
        if existing_user:
            print("User 'ravi' already exists, skipping insertion.")
            return

        # Test getting a user by ID
        user = User(username='ravi', email='ravi@example.com', role=Role.Admin, password_hash='abcxyz123', first_name='Ravi', last_name='Sharma')
        db.session.add(user)
        db.session.commit()

        response = self.client.get(f'/user/{user.id}')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['username'], 'test_user')

    # Add more test cases for other endpoints

if __name__ == '__main__':
    unittest.main()
