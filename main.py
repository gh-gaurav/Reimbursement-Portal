from flask import Flask, jsonify, render_template, session, url_for, redirect
from db import db  # Import the SQLAlchemy object from db.py
from models.user import User, Role
from models.department import Department
from models.reimbursement_request import ReimbursementRequest
from routes.user_routes import user_blueprint
from routes.department_routes import department_blueprint




app = Flask(__name__)


app.secret_key = 'your_secret_key_here'

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost/reimbursement_portal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)




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
app.register_blueprint(department_blueprint)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)