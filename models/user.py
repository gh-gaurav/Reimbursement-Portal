from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from enum import Enum

# Defining Role for the User
class Role(Enum):
    Admin = 'Admin'
    Manager = 'Manager'
    Employee = 'Employee'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    # Relationship
    department = db.relationship('Department', backref='users')
    manager = db.relationship('User', remote_side=[id], backref='employees')
    reimbursement_requests = db.relationship('ReimbursementRequest', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role.name if self.role else None,
            'department_id': self.department_id,
            'manager_id': self.manager_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
    }

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role.name}')"
