from flask import Flask, jsonify
from db import db  # Import the SQLAlchemy object from db.py
from models.user import User, Role
from models.department import Department
from models.reimbursement_request import ReimbursementRequest
from routes.user_routes import user_blueprint

app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost/reimbursement_portal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)


app.register_blueprint(user_blueprint, url_prefix='/user')

# @app.route('/create_user')
# def create_user():
#     with app.app_context():
#         new_user = User(
#             username='testuser',
#             email='testuser@example.com',
#             role=Role.Employee,
#             password='password123',
#             first_name='Test',
#             last_name='User'
#         )
#         db.session.add(new_user)
#         db.session.commit()
#         return "User created successfully!"

# @app.route('/get_users')
# def get_users():
#     with app.app_context():
#         users = User.query.all()
#         return jsonify([str(user) for user in users])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
