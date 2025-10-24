import pytest
from App.main import create_app
from App.models import db

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app  
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
