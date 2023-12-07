"""
App initialization
"""

from flask import Flask, current_app, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf import CSRFProtect

# Initialize Flask-Login
login_manager = LoginManager()
db = SQLAlchemy()
bootstrap = Bootstrap()
csrf = CSRFProtect()

def create_app(configuration=Config):
    app = Flask(__name__)
    app.config.from_object(configuration)
    csrf = CSRFProtect(app)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from app.products import bp_products
    app.register_blueprint(bp_products)

    from app.users import bp_users
    app.register_blueprint(bp_users)

    return app
from app import models

