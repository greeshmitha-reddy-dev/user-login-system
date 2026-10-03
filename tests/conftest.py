import pytest
from app import create_app, db
from app.models import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False  # Disable CSRF for unit testing simplicity

@pytest.fixture
def app():
    """Create and configure a clean Flask application instance for testing."""
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for executing HTTP requests against the application."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's CLI commands."""
    return app.test_cli_runner()

@pytest.fixture
def sample_user(app):
    """Create a sample user in the in-memory database."""
    user = User(username='testuser', email='test@example.com')
    user.set_password('Password123!')
    db.session.add(user)
    db.session.commit()
    return user
