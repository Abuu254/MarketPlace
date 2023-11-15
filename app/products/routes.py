"""
Api endpoints dealing with products
"""
from flask import render_template, redirect, flash, url_for, \
    request, g, jsonify, current_app, abort, send_from_directory
from app.products import bp_products

@bp_products.route('/')
@bp_products.route('/search', methods=['GET'])
def search():
    """Search for a product"""
    return render_template("base.html")
