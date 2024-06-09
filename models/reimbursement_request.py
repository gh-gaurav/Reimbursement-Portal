from enum import Enum
from db import db
from datetime import datetime
from sqlalchemy import event

class Category(Enum):
    Travelling = "Travelling"
    Relocation = "Relocation"
    TechAssets = "TechAssets"

class Status(Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"

class ReimbursementRequest(db.Model):
    __tablename__ = 'reimbursement_requests'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)   
    description = db.Column(db.String(255), nullable=True)
    category = db.Column(db.Enum(Category), nullable=False)
    status = db.Column(db.Enum(Status), default=Status.Pending)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Ensure 'users.id' is correct
    manager_id = db.Column(db.Integer, nullable=False)  # Ensure 'users.id' is correct
    manager_comment = db.Column(db.String(255))  # Added for manager comments
    receipt_path = db.Column(db.String(255))  # Optional field for receipt storage path
    created_on = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_on = db.Column(db.DateTime, nullable = True)

    is_active = db.Column(db.Boolean, default=True, nullable=False)  # Soft delete column

    # Define relationship with user (one-to-many)
    # requesting_user = db.relationship('User', backref='user_reimbursement_requests',lazy='True') 

    # Function to validate expense amount against category limits
    def validate_amount(self):
        category_limits = {
            Category.Travelling: 15000,
            Category.Relocation: 20000,
            Category.TechAssets: 5000
        }
        return self.amount <= category_limits[self.category]

    # Function to check if request is valid (combines validation logic)
    def is_valid(self):
        return self.validate_amount()

    def __repr__(self):
        return f"ReimbursementRequest('{self.amount}', '{self.date}', '{self.category.name}', '{self.status}')"

    
# Event listener to set created_on timestamp
@event.listens_for(ReimbursementRequest, 'before_insert')
def before_user_insert(mapper, connection, target):
    target.created_on = datetime.now()
    
# Event listener to set handled_on timestamp
@event.listens_for(ReimbursementRequest, 'before_update')
def before_user_update(mapper, connection, target):
    if target.status != "Pending" and not target.updated_on:
        target.updated_on = datetime.now()
