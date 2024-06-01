import logging
from logging.handlers import RotatingFileHandler
from config import Config

def setup_logging():
    # Set up basic logging configuration
    logging.basicConfig(level=logging.INFO)

    # Skip file rotation during testing if TESTING attribute is defined
    if hasattr(Config, 'TESTING') and Config.TESTING:
        return

    # Set up file logging with rotation
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add handler to the root logger
    logger = logging.getLogger()
    logger.addHandler(handler)

    # Log uncaught exceptions from Flask's WSGI server
    logging.getLogger('werkzeug').addHandler(handler)
    
    # Enable logging for SQLAlchemy queries
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
