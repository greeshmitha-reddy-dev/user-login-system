import pytest
from app.models import User
from app import db

def test_user_password_hashing():
    """Test that passwords are properly hashed and verified."""
    user = User(username='hash_test', email='hash@test.com')
    user.set_password('SecretPass123')
    
    assert user.password_hash != 'SecretPass123'
    assert user.check_password('SecretPass123') is True
    assert user.check_password('WrongPass') is False


def test_user_registration_success(client, app):
    """Test registering a new user account through HTTP POST."""
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'StrongPassword123',
        'confirm_password': 'StrongPassword123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Account created successfully!' in response.data
    
    with app.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'newuser@example.com'


def test_user_registration_duplicate_username(client, sample_user):
    """Test that registering with an existing username fails validation."""
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'another@example.com',
        'password': 'Password123!',
        'confirm_password': 'Password123!'
    })
    
    assert response.status_code == 200
    assert b'That username is already taken.' in response.data


def test_user_login_success(client, sample_user):
    """Test successful user login with valid credentials."""
    response = client.post('/login', data={
        'email_or_username': 'testuser',
        'password': 'Password123!'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Welcome back, testuser!' in response.data
    assert b'Authenticated Session' in response.data


def test_user_login_invalid_password(client, sample_user):
    """Test login failure with incorrect password."""
    response = client.post('/login', data={
        'email_or_username': 'testuser',
        'password': 'WrongPassword'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid username/email or password.' in response.data


def test_unauthorized_route_access(client):
    """Test that unauthenticated access to dashboard redirects to login."""
    response = client.get('/dashboard', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Please log in to access this page.' in response.data


def test_logout(client, sample_user):
    """Test user logout functionality."""
    # Login first
    client.post('/login', data={
        'email_or_username': 'testuser',
        'password': 'Password123!'
    })
    
    # Perform logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged out securely.' in response.data
