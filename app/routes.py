from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlsplit
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm, ChangePasswordForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Home landing page presenting the authentication system."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    """User Registration route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        # Instantiate user and hash password securely
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower()
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    """User Login route supporting both Username and Email login."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.email_or_username.data.strip()
        
        # Check if input matches username or email
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier.lower())
        ).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.update_last_login()
            
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Secure Open Redirect Protection
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('main.dashboard')
                
            return redirect(next_page)
        else:
            flash('Invalid username/email or password. Please try again.', 'danger')
            
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    """Logout authenticated user."""
    logout_user()
    flash('You have been logged out securely.', 'info')
    return redirect(url_for('main.login'))


@main.route('/dashboard')
@login_required
def dashboard():
    """Protected user dashboard page."""
    return render_template('dashboard.html')


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management and password change page."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Incorrect current password.', 'danger')
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated successfully!', 'success')
            return redirect(url_for('main.profile'))
            
    return render_template('profile.html', form=form)
