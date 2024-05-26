from flask import Blueprint, jsonify, request, session, url_for, redirect
from db import db
from models import User, Role, Department, ReimbursementRequest, Category, Status
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
        department_id = payload.get('department_id')
        
        
        # Fetch the admin user to get the admin's ID
        admin_user = User.query.filter_by(role=Role.Admin).first()
        if not admin_user:
            return jsonify({
                'success': False,
                'error': 'Admin user not found'
            }), 500
            
        # Set the default manager_id to the admin's ID
        manager_id = admin_user.id
        
        # validate data

        user = User(
            username=username,
            email=email,
            role=role,
            password=password,
            first_name=first_name,
            last_name=last_name,
            manager_id=manager_id,  # Set the default manager_id to admin's ID
            department_id=department_id  # Set the department_id from the payload
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


@user_blueprint.delete('/<int:id>')
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        # Soft delete: set is_active to False
        user.is_active = False

        db.session.commit()
        return jsonify({'success': True, 'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


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
        department_id = request.args.get('department_id')
        if department_id:
            users = User.query.filter(User.role == Role.Manager, User.department_id == department_id, User.is_active == True).all()
        else:
            users = User.query.filter(User.role == Role.Manager).all()
        return jsonify([{'id': user.id, 'username': user.username} for user in users]), 200
    except Exception as e:
        return f"Error: {e}"
    
@user_blueprint.get('/employees')
def get_employees():
    try:
        # users = User.query.filter(User.role.in_([Role.Employee]))
        users = User.query.filter(User.role == Role.Employee, User.is_active == True).all()  # Added .all()
        return jsonify([{'id': user.id, 'username': user.username, 'department_id': user.department_id} for user in users]), 200  # Added department_id in response
        # return jsonify([{'id': user.id, 'username': user.username} for user in users]), 200
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
        employee.manager_id = manager.id
        db.session.commit()

        return jsonify({'success' : True, 'message': 'Manager assigned successfully'}), 200

    except Exception as e:
        return jsonify({'success': False,    'error': str(e)}), 500


@user_blueprint.get('/unasigned_employees')
def unasigned_employees():
    try:
        # Fetch the admin user's ID
        admin_user = User.query.filter_by(role=Role.Admin).order_by(User.id).first()
        if not admin_user:
            return jsonify({
                'success': False,
                'error': 'Admin user not found'
            }), 500
        
        admin_id = admin_user.id
        employees = User.query.filter(User.role == Role.Employee, User.manager_id == admin_id, User.is_active == True).all()
        # employees = User.query.filter(User.role == Role.Employee, User.manager_id.is_(None)).all()
        return jsonify({'success' : True, 
                        'message': 'Employee fetched successfully', 
                        'data':[{'id': emp.id, 'username': emp.username} for emp in employees]
                        }), 200

    except Exception as e:
        return jsonify({'success': False,    'error': str(e)}), 500



# managers


@user_blueprint.get('/all')
def get_users():
    try:
        # Assuming Role is an Enum and User model has a 'role' attribute
        employees_and_managers = User.query.filter(User.role.in_([Role.Manager, Role.Employee]),User.is_active == True).all()
        
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
        if not user.is_active:
            return jsonify({'success': False, 'error': 'This account is inactive. Please contact support.'}), 401
        # Fetch department details
        department = Department.query.get(user.department_id)
        department_name = department.name if department else None
        
        session['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.value,  # Assuming user.role is an Enum
            'first_name': user.first_name,
            'last_name': user.last_name,
            'department_id':user.department_id,
            'department_name': department_name
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
    
    
    