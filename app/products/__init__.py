"""
Intialization of products blueprint
"""
from flask import Blueprint

bp_products = Blueprint('products', __name__)

from app.products import routes