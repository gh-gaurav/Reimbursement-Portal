from flask import Flask, jsonify, render_template, session, request
from db import db  # Import the SQLAlchemy object from db.py
from flask_migrate import Migrate
from routes.user_routes import user_blueprint
from routes.department_routes import department_blueprint
from routes.reimbursement_request_routes import rr_blueprint
import logging_config
from config import Config  # Import the Config class

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    migrate = Migrate(app, db)  # Initialize Flask-Migrate with your app and db
    
    # Set up logging
    logging_config.setup_logging()
    
    # Register blueprints
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(department_blueprint, url_prefix='/department')
    app.register_blueprint(rr_blueprint, url_prefix='/rr')
    
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
    
    #Context processor to make 'user' available in all templates
    @app.context_processor
    def inject_user():
        return {'user': session.get('user')}
    
    # Frontend routes
    @app.get('/')
    def root():
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
            return render_template('manager_dashboard.html', user=user)
        else:
            return render_template('access_denied.html')

    @app.get('/employee_dashboard')
    def employee_dashboard():
        user = session.get('user')
        if user and user['role'] == 'Employee':
            return render_template('employee_dashboard.html', user=user)
        else:
            return render_template('access_denied.html')

    @app.get('/admin_dashboard')
    def admin_dashboard():
        user = session.get('user')
        if user and user['role'] == 'Admin':
            return render_template('admin_dashboard.html', user=user)
        else:
            return render_template('access_denied.html')

    @app.post('/logout')
    def logout():
        session.clear()
        return jsonify({'success': True, 'message': 'Logout successful'}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
