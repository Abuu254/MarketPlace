"""
App initialization
"""

from flask import Flask, current_app, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap = Bootstrap()

def create_app(configuration=Config):
    app = Flask(__name__)
    app.config.from_object(configuration)

    db.init_app(app)
    bootstrap.init_app(app)

    from app.products import bp_products
    app.register_blueprint(bp_products)

    return app
from app import models

