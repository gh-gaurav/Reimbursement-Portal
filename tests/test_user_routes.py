import unittest
from sqlalchemy import text  # Importing text function
from flask_testing import TestCase  # type: ignore
from main import create_app, db
from models import User, Role  # Assuming Role is defined in models.py

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
            
            
            
            
            
    #creating a admin user
    def test_create_user(self):
        # Check if the user already exists
        existing_user = User.query.filter_by(username='ravi').first()
        if existing_user:
            print("User 'ravi' already exists, skipping insertion.")
            return
        #creating a user if not exist
        user = User(username='ravi', email='ravi@nucleusteq.com', role=Role.Admin, password_hash='Ravi@123', first_name='Ravi', last_name='Sharma')
        db.session.add(user)
        db.session.commit()

        # Retrieving the inserted user from the database
        user = User.query.filter_by(username='ravi').first()

        # Asserting that the user exists in the database
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'ravi')
        self.assertEqual(user.email, 'ravi@nucleusteq.com')
        # Assuming Role.Admin is defined in your Role enumeration
        self.assertEqual(user.role, Role.Admin)
        self.assertEqual(user.password_hash, 'Ravi@123')
        self.assertEqual(user.first_name, 'Ravi')
        self.assertEqual(user.last_name, 'Sharma')





    #retrieving user details
    def test_get_user(self):
        existing_user = User.query.filter_by(username='ravi').first()
        if existing_user:
            print("User 'ravi' already exists, skipping insertion.")
            return

        # Test getting a user by ID
        user = User(username='ravi', email='ravi@nucleusteq.com', role=Role.Admin, password_hash='Ravi@123', first_name='Ravi', last_name='Sharma')
        db.session.add(user)
        db.session.commit()

        response = self.client.get(f'/user/{user.id}')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['username'], 'test_user')





    #delete the user(soft_delete)
    def test_delete_user(self):
        existing_user = User.query.filter_by(username='ravi').first()
        if existing_user:
            print("User 'ravi' already exists, skipping insertion.")
            return
        #creating a user if not exist
        user = User(username='ravi', email='ravi@nucleusteq.com', role=Role.Admin, password_hash='Ravi@123', first_name='Ravi', last_name='Sharma')
        db.session.add(user)
        db.session.commit()

        # Deleting the user
        response = self.client.delete(f'/user/{user.id}')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'User deleted successfully')

        # Checking if the user is marked as inactive (soft deleted)
        deleted_user = User.query.get(user.id)
        self.assertIsNotNone(deleted_user)
        self.assertFalse(deleted_user.is_active)
        
        
        
        
        
    def test_update_user(self):
        existing_user = User.query.filter_by(username='ravi').first()
        if existing_user:
            print("User 'ravi' already exists, skipping insertion.")
            return
        # Inserting a user directly into the database for updating
        user = User(username='ravi', email='ravi@nucleusteq.com', role=Role.Admin, password_hash='Ravi@123', first_name='Ravi', last_name='Sharma')
        db.session.add(user)
        db.session.commit()

        # Updating the user
        update_data = {
            'username': 'updated_ravi',
            'email': 'updated_ravi@example.com',
            'role': 'Manager',
            'first_name': 'Updated_Ravi',
            'last_name': 'Updated_Sharma'
        }
        response = self.client.put(f'/user/{user.id}', json=update_data)
        data = response.json

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'user updated successfully')

        # Retrieving the updated user from the database
        updated_user = User.query.get(user.id)
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.username, 'updated_ravi')
        self.assertEqual(updated_user.email, 'updated_ravi@nucleusteq.com')
        self.assertEqual(updated_user.role, Role.Manager)
        self.assertEqual(updated_user.first_name, 'Updated_Ravi')
        self.assertEqual(updated_user.last_name, 'Updated_Sharma')
        
        

if __name__ == '__main__':
    unittest.main()
