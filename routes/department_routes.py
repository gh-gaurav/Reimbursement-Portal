from flask import Blueprint, jsonify, request
from models.department import Department
from db import db

department_blueprint = Blueprint('department', __name__)

@department_blueprint.route('/create', methods=['POST'])
def create_department():
    data = request.get_json()
    name = data.get('departmentName')

    if not name:
        return jsonify({'message': 'Department name is required'}), 400

    new_department = Department(name=name)
    db.session.add(new_department)
    db.session.commit()

    return jsonify({'message': 'Department created successfully', 'department': {'id': new_department.id, 'name': new_department.name}}), 201

@department_blueprint.route('/', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    return jsonify([{'id': department.id, 'name': department.name} for department in departments]), 200

@department_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_department(id):
    department = db.session.get(Department, id)

    if not department:
        return jsonify({'message': 'Department not found'}), 404

    db.session.delete(department)
    db.session.commit()

    return jsonify({'message': 'Department deleted successfully'}), 200
