from flask import Blueprint, jsonify, request
from db import db
from models import ReimbursementRequest, Category, Status
from datetime import datetime

rr_blueprint = Blueprint('reimbursement_request', __name__)

@rr_blueprint.get('/')
def ad():
    return 'das'

@rr_blueprint.post('/')
def create_reimbursement_request():
    try:
        payload = request.get_json()
        amount = payload.get('amount')
        date_str = payload.get('date')
        description = payload.get('description') or ''
        category_str = payload.get('category')
        employee_id = payload.get('employee_id')
        receipt_path = payload.get('receipt_path') or ''

        # Convert the date string to a date object
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Convert category and status strings to their respective enum types
        category = Category[category_str]

        # Create a new ReimbursementRequest object
        rr = ReimbursementRequest(
            amount=amount,
            date=date_obj,
            description=description,
            category=category,
            employee_id=employee_id,
            receipt_path=receipt_path
        )
        
        # Add and commit the record to the database
        db.session.add(rr)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Reimbursement request created successfully',
            'data': {
                'id': rr.id,
                'amount': rr.amount,
                'date': rr.date.isoformat(),
                'description': rr.description,
                'category': rr.category.value,
                'status': rr.status.value,
                'employee_id': rr.employee_id,
                'manager_comment': rr.manager_comment,
                'receipt_path': rr.receipt_path
            }
        }), 201
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@rr_blueprint.get('/')
def get_reimbursement_requests():
    requests = ReimbursementRequest.query.all()
    result = []
    for req in requests:
        result.append({
            'id': req.id,
            'amount': req.amount,
            'date': req.date.strftime('%Y-%m-%d'),
            'description': req.description,
            'category': req.category.value,
            'status': req.status.value,
            'employee_id': req.employee_id,
            'manager_comment': req.manager_comment,
            'receipt_path': req.receipt_path
        })
    return jsonify(result), 200

@rr_blueprint.put('/<int:id>')
def update_reimbursement_request(id):
    data = request.json
    req = ReimbursementRequest.query.get(id)
    if not req:
        return jsonify({'message': 'Request not found'}), 404
    
    req.status = Status[data['status']]
    req.manager_comment = data['manager_comment']
    
    db.session.commit()
    return jsonify({'message': 'Request updated successfully'}), 200

