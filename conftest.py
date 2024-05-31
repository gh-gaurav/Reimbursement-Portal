import pytest
from main import create_app
from db import db
from test_config import TestConfig

@pytest.fixture(scope='module')
def test_client():
    app = create_app(TestConfig)
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        
        yield app.test_client()  # this is where the testing happens

        db.session.remove()
        db.drop_all()
