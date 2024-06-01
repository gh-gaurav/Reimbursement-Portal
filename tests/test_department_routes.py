# tests/test_department_routes.py
import unittest
from flask_testing import TestCase
from main import create_app, db
from config import TestConfig
from models.department import Department

class TestDepartmentRoutes(TestCase):

    def create_app(self):
        return create_app(TestConfig)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_department(self):
        with self.client:
            response = self.client.post('/department/create', json={'departmentName': 'HR'})
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json['message'], 'Department created successfully')

            # Verify department is added
            departments = Department.query.all()
            self.assertEqual(len(departments), 1)
            self.assertEqual(departments[0].name, 'HR')

    def test_create_department_missing_name(self):
        with self.client:
            response = self.client.post('/department/create', json={})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json['message'], 'Department name is required')

if __name__ == '__main__':
    unittest.main()
