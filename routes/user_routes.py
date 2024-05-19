from flask import Blueprint, jsonify
from db import db
from models import User, Role

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/create')
def create_user():
    try:
        new_user = User(
            username='testuser',
            email='testuser@example.com',
            role=Role.Employee,
            password='password123',
            first_name='Test',
            last_name='User'
        )
        db.session.add(new_user)
        db.session.commit()
        return "User created successfully!"
    except Exception as e:
        return f"Error: {e}"

@user_blueprint.route('/all')
def get_users():
    try:
        users = User.query.all()
        return jsonify([str(user) for user in users])
    except Exception as e:
        return f"Error: {e}"
