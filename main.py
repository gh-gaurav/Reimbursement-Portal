from flask import Flask, jsonify, render_template, session, url_for, redirect, request
from db import db  # Import the SQLAlchemy object from db.py
from flask_migrate import Migrate
from models.user import User, Role
from models.department import Department
from models.reimbursement_request import ReimbursementRequest
from routes.user_routes import user_blueprint
from routes.department_routes import department_blueprint
from routes.reimbursement_request_routes import rr_blueprint
import logging_config




app = Flask(__name__)


app.secret_key = 'your_secret_key_here'

UPLOAD_FOLDER = 'static/receipts'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost/reimbursement_portal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)

# Initialize Flask-Migrate with your app and db
migrate = Migrate(app, db)  


# Set up logging
logging_config.setup_logging()


@app.before_request
def log_request_info():
    app.logger.info('Request Headers: %s', request.headers)
    app.logger.info('Request Body: %s', request.get_data())

@app.errorhandler(500)
def internal_error(error):
    app.logger.error('Server Error: %s', error)
    return "Internal Server Error", 500

@app.errorhandler(404)
def not_found_error(error):
    app.logger.error('Not Found: %s', error)
    return "Not Found", 404




#frontend routes

@app.get('/')
def root():
    # return "abc"
    return render_template('index.html')

@app.get('/login')
def login():
    return render_template('login.html') 

@app.get('/register')
def register():
    return render_template('registration.html') 

@app.get('/manager_dashboard')
def manager_dashboard():
    user = session.get('user')
    if user and user['role'] == 'Manager':
        return render_template('manager_dashboard.html', user=user)  # Pass the user object to the template
    else:
        return render_template('access_denied.html')  # Redirect to an access denied page if not a manager


@app.get('/employee_dashboard')
def employee_dashboard():
    user = session.get('user')
    if user and user['role'] == 'Employee':
        return render_template('employee_dashboard.html', user=user)  # Pass the user object to the template
    else:
        return render_template('access_denied.html')  # Redirect to an access denied page if not a manager

@app.get('/admin_dashboard')
def admin_dashboard():
    user = session.get('user')
    if user and user['role'] == 'Admin':
        return render_template('admin_dashboard.html', user=user)  # Pass the user object to the template
    else:
        return render_template('access_denied.html')  # Redirect to an access denied page if not a manager




@app.post('/logout')
def logout():
    session.clear()  # Clear all session data
    return jsonify({'success': True, 'message': 'Logout successful'}), 200



app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(department_blueprint, url_prefix ='/department')
app.register_blueprint(rr_blueprint, url_prefix ='/rr')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)