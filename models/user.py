from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from enum import Enum
from datetime import datetime
from sqlalchemy import event

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
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # Soft delete column
    created_on = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    deleted_on = db.Column(db.DateTime, nullable = True)
    
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
            'is_active': self.is_active
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
    
    # Event listener to set created_on timestamp
@event.listens_for(User, 'before_insert')
def before_user_insert(mapper, connection, target):
    target.created_on = datetime.now()

# Event listener to set deleted_on timestamp
@event.listens_for(User, 'before_update')
def before_user_update(mapper, connection, target):
    # print("Updating deleted_on for user:", target.id)
    if not target.is_active and not target.deleted_on:
        target.deleted_on = datetime.now()