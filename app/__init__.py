import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

# Configure LoginManager
login_manager.login_view = 'main.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

def create_app(config_class=Config):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure the instance folder exists for SQLite DB
    instance_path = os.path.join(app.root_path, '..', 'instance')
    os.makedirs(instance_path, exist_ok=True)

    # Initialize extensions with app context
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register Blueprint routes
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # User loader for Flask-Login
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create Database Tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
