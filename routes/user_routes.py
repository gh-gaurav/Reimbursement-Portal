from flask import Blueprint, jsonify, request, session, url_for, redirect
from db import db
from models import User, Role
import json

user_blueprint = Blueprint('user', __name__)

@user_blueprint.post('/')
def create_user():
    try:
        payload = request.get_json()
        username = payload.get('username')
        email = payload.get('email')
        role = payload.get('role')
        password = payload.get('password')
        first_name = payload.get('first_name')
        last_name = payload.get('last_name')

        # validate data

#hash password
        user = User(
            username=username,
            email=email,
            role=role,
            password=password,
            first_name=first_name,
            last_name=last_name
            )
        # user = User(payload)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'data' : user.to_dict() 
        }), 201
    except Exception as e:
        print(e, 123)
        return jsonify({
            'success': False,
            'error': e
        }), 400


@user_blueprint.get('/<int:id>')
def get_user(id):
    try:
        user = User.query.get(id)
        print(1223, type(user))
        if user: 
            print(user)
            return jsonify({
                'success': True,
                'message': 'User found successfully',
                'data' : user.to_dict() 
            }), 200
        else: 
            return jsonify({
                'success': False,
                'error': 'User not found',
            }), 400
            
    except Exception as e:
        print(e, 123)
        return jsonify({
            'success': False,
            'error': e
        }), 400


@user_blueprint.put('/<int:id>')
def update_user(id):
    try:
        payload = request.get_json()
        user = User.query.get(id)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        # Update user fields
        if 'username' in payload:
            user.username = payload['username']
        if 'email' in payload:
            user.email = payload['email']
        if 'role' in payload:
            user.role = Role[payload['role']]  # Assuming Role is an Enum
        if 'password' in payload:
            user.password(user, payload.password)
        if 'department_id' in payload:
            user.department_id = payload['department_id']
        if 'manager_id' in payload:
            user.manager_id = payload['manager_id']
        if 'first_name' in payload:
            user.first_name = payload['first_name']
        if 'last_name' in payload:
            user.last_name = payload['last_name']

        db.session.commit()
        return jsonify({
            'success': True, 
            'message': 'user updated successfully',
            'data': user.to_dict(), 
            }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400



@user_blueprint.get('/managers')
def get_managers():
    try:
        users = User.query.filter(User.role.in_([Role.Manager]))
        return jsonify([{'id': user.id, 'username': user.username} for user in users]), 200
    except Exception as e:
        return f"Error: {e}"
    
@user_blueprint.get('/employees')
def get_employees():
    try:
        users = User.query.filter(User.role.in_([Role.Employee]))
        return jsonify([{'id': user.id, 'username': user.username} for user in users]), 200
    except Exception as e:
        return f"Error: {e}"

@user_blueprint.post('/assign-manager')
def assign_manager():
    try:
        data = request.json
        manager_id = data.get('managerId')
        employee_id = data.get('employeeId')

        # Fetch manager and employee objects from the database
        manager = User.query.get(manager_id)
        employee = User.query.get(employee_id)

        if not manager:
            return jsonify({'error': 'Manager not found'}), 404
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404

        # Assign the manager to the employee
        employee.manager = manager
        db.session.commit()

        return jsonify({'success' : True, 'message': 'Manager assigned successfully'}), 200

    except Exception as e:
        return jsonify({'success': False,    'error': str(e)}), 500


@user_blueprint.get('/unasigned_employees')
def unasigned_employees():
    try:
        employees = User.query.filter(User.role == Role.Employee, User.manager_id.is_(None)).all()
        return jsonify({'success' : True, 'message': 'Employee fetched successfully', 'data':[{'id': emp.id, 'username': emp.username} for emp in employees]}), 200

    except Exception as e:
        return jsonify({'success': False,    'error': str(e)}), 500



# managers


@user_blueprint.get('/all')
def get_users():
    try:
        # Assuming Role is an Enum and User model has a 'role' attribute
        employees_and_managers = User.query.filter(User.role.in_([Role.Manager, Role.Employee])).all()
        
        # Initialize empty arrays for managers and employees
        managers = []
        employees = []

        # Iterate through the users and append them to the appropriate array based on their role
        for user in employees_and_managers:
            if user.role == Role.Manager:
                managers.append(user.to_dict())
            elif user.role == Role.Employee:
                employees.append(user.to_dict())

        # Return both arrays as JSON
        return jsonify({
            'managers': managers,
            'employees': employees
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@user_blueprint.post('/login')
def login():
    data = request.json  # Get the JSON data from the request
    username_or_email = data.get('username')  # Assuming the input field is named 'username'
    password = data.get('password')

    # Check if username_or_email is an email
    if '@' in username_or_email:
        user = User.query.filter_by(email=username_or_email).first()
    else:
        user = User.query.filter_by(username=username_or_email).first()

    if user and user.verify_password(password):
        session['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.value,  # Assuming user.role is an Enum
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        # Authentication successful
        if user.role == Role.Manager:
            return jsonify({'success': True, 'message': 'Login successful', 'redirect': '/manager_dashboard'}), 200
        elif user.role == Role.Employee:
            return jsonify({'success': True, 'message': 'Login successful', 'redirect': '/employee_dashboard'}), 200
        elif user.role == Role.Admin:
            return jsonify({'success': True, 'message': 'Login successful', 'redirect': '/admin_dashboard'}), 200        
        else:
            return jsonify({'success': False, 'error': 'Invalid user role'}), 401
    else:
        # Authentication failed
        return jsonify({'success': False, 'error': 'Login failed. Please check your credentials.'}), 401


