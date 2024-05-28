from flask import Blueprint, jsonify, request, current_app
from db import db
from models import ReimbursementRequest, Category, Status, User, Role
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import uuid

rr_blueprint = Blueprint('reimbursement_request', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@rr_blueprint.post('/')
def create_reimbursement_request():
    try:
        amount = request.form.get('amount')
        date_str = request.form.get('date')
        description = request.form.get('description') or ''
        category_str = request.form.get('category')
        employee_id = request.form.get('employee_id')

        if 'receipt' not in request.files:
            return jsonify({'success': False, 'error': 'No receipt file provided'}), 400

        receipt_files = request.files.getlist('receipt')
        request_id = str(uuid.uuid4())
        request_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], request_id)
        os.makedirs(request_dir, exist_ok=True)
        receipt_paths = []

        for receipt_file in receipt_files:
            if receipt_file.filename == '':
                return jsonify({'success': False, 'error': 'No selected file'}), 400

            if receipt_file and allowed_file(receipt_file.filename):
                filename = secure_filename(receipt_file.filename)
                receipt_path = os.path.join(request_dir, filename)
                receipt_file.save(receipt_path)
                receipt_paths.append(receipt_path)
            else:
                return jsonify({'success': False, 'error': 'File type not allowed'}), 400

        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        category = Category[category_str]
        emp_data = User.query.get(employee_id)

        rr = ReimbursementRequest(
            amount=amount,
            date=date_obj,
            description=description,
            category=category,
            employee_id=employee_id,
            receipt_path=','.join(receipt_paths),
            manager_id=emp_data.manager_id
        )

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
                'receipt_path': request_id
            }
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400



@rr_blueprint.get('/get_reimbursement_requests_manager')
def get_reimbursement_requests_manager():
    manager_id = request.args['manager_id']
    # print(224, manager_id)
    # requests = ReimbursementRequest.query.all()
    requests = ReimbursementRequest.query.filter_by(manager_id=manager_id,is_active=True).all()
    # manager_id = manager_id,
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
    req.is_active = False
    
    db.session.commit()
    return jsonify({'message': 'Request updated successfully', 'is_active': req.is_active}), 200




#for employee
@rr_blueprint.get('/get_reimbursement_requests_employee')
def get_reimbursement_requests_employee():
    employee_id = request.args['employee_id']
    requests = ReimbursementRequest.query.filter_by(employee_id=employee_id).all()
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
    return jsonify({"success": True, "data": result}), 200



#for admin
@rr_blueprint.get('/get_reimbursement_requests_admin')
def get_reimbursement_requests_admin():
    try:
        admin_user = User.query.filter_by(role=Role.Admin, is_active=True).first()
        admin_id = admin_user.id
        requests = ReimbursementRequest.query.join(
            User,ReimbursementRequest.manager_id==User.id).filter(
            ReimbursementRequest.manager_id == admin_id,ReimbursementRequest.is_active == True).all()
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
                'manager_id': req.manager_id,
                'manager_comment': req.manager_comment,
                'receipt_path': req.receipt_path
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@rr_blueprint.get('/get_reimbursement_requests')
def get_reimbursement_requests():
    try:
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
                'manager_id': req.manager_id,
                'manager_comment': req.manager_comment,
                'receipt_path': req.receipt_path
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
