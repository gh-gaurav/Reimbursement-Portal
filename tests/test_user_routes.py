import unittest
from flask import Flask
from config import TestConfig
from main import create_app
from db import db
from models import User, Role

class TestUserRoutes(unittest.TestCase):
    def setUp(self):
        """Set up the test client and initialize the test database."""
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app.app_context().push()
        db.create_all()

        # Add an admin user to the database for testing
        admin_user = User(
            username='admin',
            email='admin@example.com',
            role=Role.Admin,
            password='adminpass',
            first_name='Admin',
            last_name='User'
        )
        db.session.add(admin_user)
        db.session.commit()

    def tearDown(self):
        """Tear down the test database."""
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        """Test creating a new user."""
        # Define the payload for the POST request
        payload = {
            'username': 'testuser',
            'email': 'testuser@nucleusteq.com',
            'role': 'Employee',
            'password': 'Testuser@123',
            'first_name': 'Test',
            'last_name': 'User',
            'department_id': 1  # Assuming department ID 1 exists in the test DB
        }

        # Make the POST request to create the user
        response = self.client.post('/user/', json=payload)

        # Parse the response data
        data = response.get_json()

        # Assert the response status code and message
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'User created successfully')
        self.assertIn('data', data)
        self.assertEqual(data['data']['username'], 'testuser')
        self.assertEqual(data['data']['email'], 'testuser@nucleusteq.com')
        self.assertEqual(data['data']['role'], 'Employee')
        self.assertEqual(data['data']['first_name'], 'Test')
        self.assertEqual(data['data']['last_name'], 'User')


    def test_get_user(self):
        """Test retrieving a user by ID."""
        # Create a user to retrieve
        new_user = User(
            username='anotheruser',
            email='anotheruser@nucleusteq.com',
            role=Role.Employee,
            password='Anotheruser@123',
            first_name='Another',
            last_name='User',
            department_id=1
        )
        db.session.add(new_user)
        db.session.commit()

        # Make the GET request to retrieve the user
        response = self.client.get(f'/user/{new_user.id}')
        data = response.get_json()

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['username'], 'anotheruser')
        self.assertEqual(data['data']['email'], 'anotheruser@nucleusteq.com')
        self.assertEqual(data['data']['role'], 'Employee')
        self.assertEqual(data['data']['first_name'], 'Another')
        self.assertEqual(data['data']['last_name'], 'User')


    def test_update_user(self):
        """Test updating an existing user."""
        # Create a user to update
        new_user = User(
            username='updateuser',
            email='updateuser@nucleusteq.com',
            role=Role.Employee,
            password='Updateuser@123',
            first_name='Update',
            last_name='User',
            department_id=1
        )
        db.session.add(new_user)
        db.session.commit()

        # Define the payload for the PUT request to update the user
        updated_payload = {
            'first_name': 'Updated',
            'last_name': 'UserUpdated',
        }

        # Make the PUT request to update the user
        response = self.client.put(f'/user/{new_user.id}', json=updated_payload)
        data = response.get_json()

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'user updated successfully')  # Corrected message case

        # Fetch the updated user from the database
        updated_user = User.query.get(new_user.id)

        # Assert the updated user attributes
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'UserUpdated')
        
    def test_delete_user(self):
        """Test deleting a user."""
        # Create a user to delete
        new_user = User(
            username='deleteuser',
            email='deleteuser@nucleusteq.com',
            role=Role.Employee,
            password='Deleteuser@123',
            first_name='Delete',
            last_name='User',
            department_id=1
        )
        db.session.add(new_user)
        db.session.commit()

        # Make the DELETE request to delete the user
        response = self.client.delete(f'/user/{new_user.id}')
        data = response.get_json()

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'User deleted successfully')

        # Ensure the user is marked as inactive in the database
        deleted_user = User.query.get(new_user.id)
        self.assertFalse(deleted_user.is_active)

    def test_assign_manager(self):
        """Test assigning a manager to an employee."""
        # Create an admin user (manager)
        admin_user = User(
            username='admin1',
            email='admin1@nucleusteq.com',
            role=Role.Admin,
            password='admin1@123',
            first_name='Admin1',
            last_name='User1'
        )
        db.session.add(admin_user)
        db.session.commit()

        # Create an employee to assign manager to
        employee = User(
            username='emp1',
            email='emp1@nucleusteq.com',
            role=Role.Employee,
            password='emp1pass',
            first_name='Emp',
            last_name='One',
            department_id=1
        )
        db.session.add(employee)
        db.session.commit()

        # Define payload for assigning manager
        payload = {
            'managerId': admin_user.id,
            'employeeId': employee.id
        }

        # Make the POST request to assign manager
        response = self.client.post('/user/assign-manager', json=payload)
        data = response.get_json()

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Manager assigned successfully')

        # Fetch the updated employee from the database
        updated_employee = User.query.get(employee.id)

        # Assert the manager_id is updated correctly
        self.assertEqual(updated_employee.manager_id, admin_user.id)
        
    def test_get_employees_for_manager(self):
        """Test retrieving employees for a manager."""
        # Create a manager user
        manager_user = User(
            username='manager1',
            email='manager1@nucleusteq.com',
            role=Role.Manager,
            password='Manager1@123',
            first_name='Manager1',
            last_name='User',
            department_id=1
        )
        db.session.add(manager_user)
        db.session.commit()

        # Create employees under the manager
        employee1 = User(
            username='emp2',
            email='emp2@nucleusteq.com',
            role=Role.Employee,
            password='Emp2@123',
            first_name='Emp2',
            last_name='One',
            department_id=1,
            manager_id=manager_user.id
        )
        employee2 = User(
            username='emp3',
            email='emp3@nucleusteq.com',
            role=Role.Employee,
            password='Emp3@123',
            first_name='Emp3',
            last_name='Two',
            department_id=1,
            manager_id=manager_user.id
        )
        db.session.add_all([employee1, employee2])
        db.session.commit()

        # Make the GET request to retrieve employees for the manager
        response = self.client.get(f'/user/get_employees_for_manager?manager_id={manager_user.id}')
        data = response.get_json()

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 2)  # Assuming 2 employees are returned
        self.assertTrue(all(employee['manager_id'] == manager_user.id for employee in data['data']))


    def test_get_managers(self):
        """Test retrieving managers optionally filtered by department."""
        # Create managers in different departments
        manager1 = User(
            username='manager2',
            email='manager2@nucleusteq.com',
            role=Role.Manager,
            password='manager2@123',
            first_name='Manager2',
            last_name='One',
            department_id=1  # Department ID 1
        )
        manager2 = User(
            username='manager3',
            email='manager3@nucleusteq.com',
            role=Role.Manager,
            password='Manager3@123',
            first_name='Manager',
            last_name='Two',
            department_id=2  # Department ID 2
        )
        db.session.add_all([manager1, manager2])
        db.session.commit()

        # Make the GET request to retrieve managers without department filter
        response = self.client.get('/user/managers')
        data = response.get_json()

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 2)  # Assuming there are 2 managers in total

        # Make the GET request to retrieve managers filtered by department ID
        response = self.client.get('/user/managers?department_id=1')
        data = response.get_json()

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)  # Assuming only 1 manager in department ID 1
        self.assertEqual(data[0]['id'], manager1.id)


    
    def test_get_all_users(self):
        """Test retrieving all users categorized as managers and employees."""
        # Create both managers and employees
        manager1 = User(
            username='manager4',
            email='manager4@nucleusteq.com',
            role=Role.Manager,
            password='Manager4@123',
            first_name='Manager4',
            last_name='One',
            department_id=1
        )
        employee1 = User(
            username='employee4',
            email='employee4@nucleusteq.com',
            role=Role.Employee,
            password='Employee4@123',
            first_name='Employee',
            last_name='One',
            department_id=1
        )
        db.session.add_all([manager1, employee1])
        db.session.commit()

        # Make the GET request to retrieve all users
        response = self.client.get('/user/all')
        data = response.get_json()

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertTrue('managers' in data)
        self.assertTrue('employees' in data)
        self.assertEqual(len(data['managers']), 1)  # Assuming 1 manager
        self.assertEqual(len(data['employees']), 1)  # Assuming 1 employee
        
    def test_login_failed(self):
        """Test login with incorrect credentials."""
        # Create a user for testing
        user = User(
            username='loginuser',
            email='loginuser@nucleusteq.com',
            role=Role.Employee,
            password='Loginuser@123',
            first_name='Login',
            last_name='User',
            department_id=1
        )
        db.session.add(user)
        db.session.commit()

        # Attempt login with incorrect password
        payload = {
            'username': 'loginuser',
            'password': 'wrongpassword'
        }
        response = self.client.post('/user/login', json=payload)
        data = response.get_json()

        # Assert the response status code and data
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Login failed. Please check your credentials.')



if __name__ == '__main__':
    unittest.main()
