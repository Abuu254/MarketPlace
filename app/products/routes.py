"""
Api endpoints dealing with products
"""
from datetime import datetime
from sqlalchemy import or_
from flask import render_template, redirect, flash, url_for, \
    request, g, jsonify, current_app, abort, send_from_directory
from app.products import bp_products
from app.models import User, Product, Category, Image, Address
from app import db
from sqlalchemy.orm import joinedload

@bp_products.route('/')
@bp_products.route('/index', methods=['GET'])
def index():
    categories = Category.query.all()
    return render_template("index.html", categories=categories)

@bp_products.route('/ajax_search', methods=['GET'])
def ajax_search():
    query = request.args.get('search_query', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = 20

    category_id = request.args.get('category')
    condition = request.args.get('condition')
    date_posted_str = request.args.get('date_posted')
    status = request.args.get('status')
    price_order = request.args.get('price')

    query_obj = Product.query

    # Split query into individual words
    search_terms = query.split()

    if query:
        # Construct an OR condition for each search term
        search_conditions = [Product.ProductName.ilike(f'%{term}%') for term in search_terms]
        query_obj = query_obj.filter(or_(*search_conditions))

    # if query:
    #     query_obj = query_obj.filter(Product.ProductName.contains(query))
    if category_id and category_id != 'any':
        query_obj = query_obj.filter(Product.CategoryID == category_id)
    if condition and condition != 'any':
        query_obj = query_obj.filter(Product.Condition == condition)

    # Date filtering logic
    if date_posted_str:
        try:
            date_posted = datetime.strptime(date_posted_str, '%Y-%m-%d')
            query_obj = query_obj.filter(Product.DatePosted >= date_posted)
        except ValueError:
            pass  # Invalid date format, ignore the filter

    # Status filtering logic
    if status:
        is_sold = status.lower() == 'sold'
        query_obj = query_obj.filter(Product.IsSold == is_sold)

    # Price sorting
    if price_order == 'asc':
        query_obj = query_obj.order_by(Product.Price.asc())
    elif price_order == 'desc':
        query_obj = query_obj.order_by(Product.Price.desc())

    products_pagination = query_obj.options(joinedload(Product.images)).paginate(page, per_page, False)

    products = products_pagination.items
    product_list = []
    for product in products:
        first_image_url = url_for('static', filename='path/to/default/image.jpg') if not product.images else product.images[0].ImageURL

        product_data = {
            'id': product.ProductID,
            'name': product.ProductName,
            'description': product.Description,
            'color': product.ProductColor,
            'condition': product.Condition,
            'date_posted': product.DatePosted.strftime('%Y-%m-%d'),
            'price': product.Price,
            'image_url': first_image_url
        }
        product_list.append(product_data)

    product_list_with_pagination = {
        'products': product_list,
        'pagination': {
            'has_next': products_pagination.has_next,
            'has_prev': products_pagination.has_prev,
            'next_num': products_pagination.next_num,
            'prev_num': products_pagination.prev_num,
            'total_pages': products_pagination.pages,
            'current_page': products_pagination.page
        }
    }

    return jsonify(product_list_with_pagination)
