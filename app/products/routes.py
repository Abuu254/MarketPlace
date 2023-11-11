"""
Api endpoints dealing with products
"""
from app.products import bp_products

@bp_products.route('/')
@bp_products.route('/search', methods=['GET'])
def search():
    """Search for a product"""

