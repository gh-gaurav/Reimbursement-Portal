import os
import unittest
import tempfile
from main import create_app, db
from models import User, Role
from config import TestConfig

class TestReimbursementRequestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

        with self.app.app_context():
            db.create_all()
            self.create_test_data()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_data(self):
        manager = User(
            username='manager',
            email='manager@example.com',
            role=Role.Manager,
            password_hash='test',
            first_name='Manager',
            last_name='User',
            is_active=True
        )
        db.session.add(manager)
        db.session.commit()

        user = User(
            username='test_user',
            email='test_user@example.com',
            role=Role.Employee,
            password_hash='test',
            first_name='Test',
            last_name='User',
            is_active=True,
            manager_id=manager.id
        )
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id
        self.manager_id = manager.id

    def test_create_reimbursement_request(self):
        with self.app.app_context():
            data = {
                'amount': '1000',
                'date': '2023-01-01',
                'description': 'Business trip',
                'category': 'Travelling',
                'employee_id': self.user_id
            }
            # Create a sample receipt file
            receipt_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            receipt_file.write(b'Test receipt content')
            receipt_file.close()

            with open(receipt_file.name, 'rb') as f:
                data['receipt'] = f
                response = self.client.post(
                    '/rr/',
                    data=data,
                    content_type='multipart/form-data'
                )

            self.assertEqual(response.status_code, 201)
            self.assertIn('Reimbursement request created successfully', response.get_data(as_text=True))
            
            # Clean up
            os.remove(receipt_file.name)

if __name__ == '__main__':
    unittest.main()
