from flask import Blueprint, render_template, request
from models.product import get_products_by_category

category_bp = Blueprint('category', __name__)

@category_bp.route('/electronics')
def electronics():
    search_query = request.args.get("search", "").strip().lower()
    products = get_products_by_category('electronics', search_query)
    
    return render_template('electronics.html', products=products, search_query=search_query)

@category_bp.route('/computer')
def computer():
    search_query = request.args.get("search", "").strip().lower()
    products = get_products_by_category('computer', search_query)
    
    return render_template('computer.html', products=products, search_query=search_query)

@category_bp.route('/kitchen')
def kitchen():
    search_query = request.args.get("search", "").strip().lower()
    products = get_products_by_category('home', search_query)
    
    return render_template('kitchen.html', products=products, search_query=search_query)


# @category_bp.route("/electronics")
# def electronics():
#     conn = sqlite3.connect("my_database.db")
#     conn.row_factory = sqlite3.Row
#     cursor = conn.cursor()

#     # Get search query from the request parameters
#     search_query = request.args.get("search", "").strip().lower()

#     # Base SQL query
#     sql_query = "SELECT product_id, product_name, actual_price, img_link FROM products WHERE LOWER(category) LIKE 'electronics%'"
#     query_params = []

#     # If there's a search query, modify the SQL to filter results
#     if search_query:
#         sql_query += " AND LOWER(product_name) LIKE ?"
#         query_params.append(f"%{search_query}%")

#     cursor.execute(sql_query, query_params)
#     rows = cursor.fetchall()

#     # Convert rows to a list of dictionaries
#     products = [dict(row) for row in rows]

#     print("DEBUG: Products fetched from DB:", products)  # Debugging log

#     conn.close()
#     return render_template('electronics.html', products=products, search_query=search_query)


# @app.route("/computer")
# def computer():
#     conn = sqlite3.connect("my_database.db")
#     conn.row_factory = sqlite3.Row
#     cursor = conn.cursor()

#     # Get search query from the request parameters
#     search_query = request.args.get("search", "").strip().lower()

#     # Base SQL query
#     sql_query = "SELECT product_id, product_name, actual_price, img_link FROM products WHERE LOWER(category) LIKE 'computer%'"
#     query_params = []

#     # If there's a search query, modify the SQL to filter results
#     if search_query:
#         sql_query += " AND LOWER(product_name) LIKE ?"
#         query_params.append(f"%{search_query}%")

#     cursor.execute(sql_query, query_params)
#     rows = cursor.fetchall()

#     # Convert rows to a list of dictionaries
#     products = [dict(row) for row in rows]

#     print("DEBUG: Products fetched from DB:", products)  # Debugging log

#     conn.close()
#     return render_template('electronics.html', products=products, search_query=search_query)


# @app.route("/kitchen")
# def kitchen():
#     conn = sqlite3.connect("my_database.db")
#     conn.row_factory = sqlite3.Row
#     cursor = conn.cursor()

#     # Get search query from the request parameters
#     search_query = request.args.get("search", "").strip().lower()

#     # Base SQL query
#     sql_query = "SELECT product_id, product_name, actual_price, img_link FROM products WHERE LOWER(category) LIKE 'home%'"
#     query_params = []

#     # If there's a search query, modify the SQL to filter results
#     if search_query:
#         sql_query += " AND LOWER(product_name) LIKE ?"
#         query_params.append(f"%{search_query}%")

#     cursor.execute(sql_query, query_params)
#     rows = cursor.fetchall()

#     # Convert rows to a list of dictionaries
#     products = [dict(row) for row in rows]

#     print("DEBUG: Products fetched from DB:", products)  # Debugging log

#     conn.close()
#     return render_template('electronics.html', products=products, search_query=search_query)
