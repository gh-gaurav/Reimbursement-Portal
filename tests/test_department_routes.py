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

    def test_get_departments(self):
        # Inserting some departments into the database
        department1 = Department(name='IT')
        department2 = Department(name='Finance')
        db.session.add_all([department1, department2])
        db.session.commit()

        with self.client:
            response = self.client.get('/department/')
            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertEqual(len(data), 2)  # Assuming we have exactly 2 departments
            self.assertEqual(data[0]['name'], 'IT')
            self.assertEqual(data[1]['name'], 'Finance')

    def test_delete_department(self):
        # Insert a department into the database
        department = Department(name='HR')
        db.session.add(department)
        db.session.commit()

        with self.client:
            response = self.client.delete(f'/department/{department.id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Department deleted successfully')

            # Verify department is deleted
            deleted_department = Department.query.get(department.id)
            self.assertIsNone(deleted_department)

if __name__ == '__main__':
    unittest.main()
