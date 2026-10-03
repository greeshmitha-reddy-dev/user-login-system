from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from app.models import User

class RegistrationForm(FlaskForm):
    """User Registration Form with strict input validation."""
    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=3, max=30, message='Username must be between 3 and 30 characters.'),
        Regexp('^[A-Za-z0-9_]+$', message='Username can only contain letters, numbers, and underscores.')
    ])
    
    email = StringField('Email Address', validators=[
        DataRequired(message='Email address is required.'),
        Email(message='Please enter a valid email address.')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=8, message='Password must be at least 8 characters long.')
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password.'),
        EqualTo('password', message='Passwords must match.')
    ])
    
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        """Ensure username is unique."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose another.')

    def validate_email(self, email):
        """Ensure email address is unique (case-insensitive)."""
        user = User.query.filter(User.email.ilike(email.data)).first()
        if user:
            raise ValidationError('An account with this email already exists.')


class LoginForm(FlaskForm):
    """User Login Form supporting Username or Email authentication."""
    email_or_username = StringField('Email or Username', validators=[
        DataRequired(message='Please enter your username or email address.')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.')
    ])
    
    remember_me = BooleanField('Remember Me')
    
    submit = SubmitField('Sign In')


class ChangePasswordForm(FlaskForm):
    """Password update form for authenticated users."""
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message='Current password is required.')
    ])
    
    new_password = PasswordField('New Password', validators=[
        DataRequired(message='New password is required.'),
        Length(min=8, message='New password must be at least 8 characters long.')
    ])
    
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Please confirm your new password.'),
        EqualTo('new_password', message='New passwords must match.')
    ])
    
    submit = SubmitField('Update Password')
