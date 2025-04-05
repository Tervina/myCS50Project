from flask import Blueprint, render_template
from repository.product import get_product_by_id

product_bp = Blueprint('product', __name__)

# @app.route('/product/<string:product_id>')
# def product_details(product_id):
#     conn = sqlite3.connect("my_database.db")
#     cursor = conn.cursor()

#     #Fetch product details based on product_id
#     cursor.execute("SELECT product_id, product_name, category, discounted_price, actual_price, discount_percentage, rating, img_link, about_product FROM products WHERE product_id = ?",(product_id,))
#     product = cursor.fetchone() #get a single product

#     conn.close()

#     if product is None:
#         return "product not found",404 #handle invalid product_id

#     return render_template("product.html",product = product)

@product_bp.route('/product/<string:product_id>')
def product_details(product_id):
    product = get_product_by_id(product_id)
    
    if product is None:
        return "Product not found", 404
    
    return render_template("product.html", product=product)