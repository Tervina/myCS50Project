from flask import Flask, render_template, request, jsonify, session, redirect, url_for,g,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sock import Sock        #lets you use WebSockets to send and receive messages in real-time without refreshing the page
from flask_session import Session  # Import session extension
import sqlite3,json
import random
import requests
import secrets,os
from flask_wtf.csrf import CSRFProtect
from flask import session
from flask_session import Session
import re
from flask import request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


print(secrets.token_hex(32))  # Generates a secure 32-byte key
app = Flask(__name__)
# Configure session
#Instead of hardcoding the key, store it in an environment variable
# app.secret_key = "30dc62dc9f43c1410154a6cc394fd3f48bc6fb65cba19c7b8a876376ec84b2bf"
app.secret_key = os.getenv("SECRET_KEY", "fallback_default_key")
# Enable CSRF protection
csrf = CSRFProtect(app)
CART_FILE = "cart.json"  # JSON file to store cart data

# EMAIL_PASSWORD = os.environ.get("Vina123!") 

EMAIL_PASSWORD = "yzbo xwbc wrfq aicj"
# Ensure session keys exist
@app.before_request
def initialize_session():
    if "cart" not in session:
        session["cart"] = []
    if "cart_count" not in session:
        session["cart_count"] = 0

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"  # Store session data in files
Session(app)  # Initialize Flask session management
sock = Sock(app)

app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production
app.config['WTF_CSRF_ENABLED'] = True  # Ensure CSRF is enabled

# Function to clean price string
def clean_price(price_str):
    clean = re.sub(r'[^\d.]', '', price_str)  # Remove currency symbols like ₹, commas, etc.
    return float(clean) if clean else 0.0

# Fallback image URL (stored in static/images/)
PLACEHOLDER_IMAGE = "static/images/out_of_stock.png"

def is_valid_image_url(url):
    """Check if an image URL is reachable (HTTP status 200)"""
    try:
        response = requests.head(url, timeout=3)  # Send a HEAD request (faster than GET)
        return response.status_code == 200  # Return True if image exists
    except requests.RequestException:
        return False  # If request fails, return False

# Function to get a product by ID
def get_product_by_id(product_id):
    for product in products:
        if product['product_id'] == product_id:
            return product
    return None  # If not found

#Fetch random products from the database in your Flask backend.
def get_random_products(limit = 10):
    conn = sqlite3.connect("my_database.db")

    # Create a cursor object to execute queries
    cursor = conn.cursor()

    # Fetch all products from the database
    cursor.execute("SELECT product_id,product_name,category,discounted_price,actual_price,discount_percentage,rating,img_link FROM products;")
    
    # Get all products as a list of tuples
    products = cursor.fetchall()

    conn.close() # Close the database connection
    if not products:  # Handle empty database
        return []
    # Select 'limit' number of random products
    random_products = random.sample(products, min(limit, len(products))) if products else []
     # Validate image URLs before returning
    validated_products = []
    for product in random_products:
        product_id, name, category, discounted_price, actual_price, discount_percentage, rating, img_link = product
        valid_img_link = img_link if is_valid_image_url(img_link) else PLACEHOLDER_IMAGE
        validated_products.append((product_id, name, category, discounted_price, actual_price, discount_percentage, rating, valid_img_link))

    return validated_products

@app.route("/")
def index():
    if "user" in session:  # If user is already logged in
        return redirect(url_for("home"))
    
    return redirect(url_for("login"))

@sock.route('/reload')
def reload(ws):
    while True:
        ws.receive()
        ws.send('reload')

# Route to insert user data
# @app.route('/register', methods=['GET','POST'])
# def register():
#     if request.method == 'GET':
#         return render_template("register.html")
#     try:
#         data = request.get_json()  # Get JSON data from request
#         print(data)
#         if data is None:
#             return jsonify({"error": "Invalid or missing JSON data"}), 400
        
#         user_name = data['user_name']
#         email = data['email']
#         password = data['password']
#         # user_name = request.form['user_name']
#         # email = request.form['email']
#         # password = request.form['password']
#         print(request.data)  # Check raw request data
#         if not user_name or not email or not password:
#             return jsonify({"error": "Missing required fields"}), 400
        
#         conn = sqlite3.connect("my_database.db")
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO user (user_name, email, password) VALUES (?, ?, ?)",
#                        (user_name, email, password))
#         conn.commit()
#         conn.close()

#         return jsonify({"message": "User registered successfully!"}), 201

#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
    
    # return render_template('register.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    try:
        print("Headers:", request.headers)  
        print("Raw Data Received:", request.data)  # Debugging  

        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        user_name = data.get('user_name')
        # age = data.get('age', '')  # Default to empty if not provided
        # address = data.get('address', '')  
        email = data.get('email')
        password = data.get('password')

        if not user_name or not email or not password:
            return jsonify({"error": "Missing required fields"}), 400

        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user (user_name, email, password) VALUES (?, ?, ?)",
                       (user_name,email, password))
        conn.commit()
        conn.close()

        return jsonify({"message": "User registered successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user" in session:  # Check if user is already logged in
        return redirect(url_for("home"))  # Redirect to home
    
    if request.method == 'GET':
        return render_template("login.html")  # Serve login page

    try:
        data = request.json
        user_name = data.get("user_name")
        password = data.get("password")

        print("Received login data:", data)  # Debugging: Print received data

        if not data:
            return jsonify({"error": "No data received"}), 400
        
      

        if not user_name or not password:
            return jsonify({"error": "Please enter both username and password"}), 400

        with sqlite3.connect("my_database.db") as conn:
            cursor = conn.cursor()
            # hashed_password = generate_password_hash(password)  # Hash the new password

            cursor.execute("SELECT password, user_id FROM user WHERE user_name = ?", (user_name,))
            user = cursor.fetchone()

            if user:
                print("User found:", user)  # Debugging: Print user info
            else:
                return jsonify({"error": "User not found"}), 404  # Handle missing user
  
            if user:
                db_password = user[0]  # Fix: Accessing password using index
                user_id = user[1]  # Get user_id from database
        
                if password == db_password:
                    session['user'] = user_name  # Set "user" key in session
                    session['user_id'] = user_id  # Store user_id in session
                    print(f"User {user_name} logged in successfully!")
                    return jsonify({"message": "Login successful", "redirect": "/home"}), 200
                else:
                    return jsonify({"error": "Invalid username or password"}), 401
            else:
                return jsonify({"error":"user not found"}),404
    except Exception as e:
        print("Login error:", str(e))  # Debugging: Print error
        return jsonify({"error": str(e)}), 500


@app.route('/logout')
def logout():
    session.pop("user_id", None)
    session.clear()  # ✅ Clear all session data  # Remove user session
    return redirect(url_for("login"))

@app.route('/forget-pass',methods = ['GET','POST'])
def forget():
    if request.method == 'GET':
        return render_template("forget-pass.html")
    try:
        data = request.json;
        email= data['email']
        new_password = data['new_password']

        if not email or not new_password:
            return jsonify({"error": "Please provide both email and new password"}), 400
       
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "Email not found"}), 404  # No user with that email

        # hashed_password = generate_password_hash(new_password)  # Hash the new password

        cursor.execute("UPDATE user SET password = ? WHERE email = ?", (new_password, email))

        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
                return jsonify({"error": "Email not found"}), 404  # No user with that email
        
        return jsonify({"message": "Password updated successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400



@app.route('/home')
def home():
    if "user_id" not in session:  # If user is not logged in
        return redirect(url_for("login"))  # Redirect to login
    
    products = get_random_products()  # Fetch 5 random products

    return render_template("home.html",products=products)

@app.route('/product/<string:product_id>')
def product_details(product_id):
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()

    #Fetch product details based on product_id
    cursor.execute("SELECT product_id, product_name, category, discounted_price, actual_price, discount_percentage, rating, img_link, about_product FROM products WHERE product_id = ?",(product_id,))
    product = cursor.fetchone() #get a single product

    conn.close()

    if product is None:
        return "product not found",404 #handle invalid product_id

    return render_template("product.html",product = product) 

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity', 1)

    # Get user_id from session
    user_id = session.get('user_id')  
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401  # Unauthorized

    # Open database connection
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()

    # Fetch product details
    product = cursor.execute(
        "SELECT product_id, product_name, actual_price FROM products WHERE product_id = ?",
        (product_id,)
    ).fetchone()

    if not product:
        conn.close()
        return jsonify({"error": "Product not found"}), 404

    # ✅ Ensure actual_price is numeric by removing ₹ symbol and commas
    raw_price = product[2] if product[2] is not None else "0"
    try:
        cleaned_price = float(raw_price.replace("₹", "").replace(",", "").strip())
    except ValueError:
        cleaned_price = 0.0  # Default price if conversion fails

    # Check if the product is already in the cart
    cursor.execute("SELECT quantity FROM cart WHERE user_id = ? AND product_id = ?", (user_id, product_id))
    existing_product = cursor.fetchone()

    if existing_product:
        # If product exists, update the quantity
        new_quantity = existing_product[0] + quantity
        cursor.execute("UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?", (new_quantity, user_id, product_id))
    else:
        # If product does not exist, insert new row
        cursor.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
            (user_id, product_id, quantity)
        )

    # Commit changes & close connection
    conn.commit()
    conn.close()

    # Update session cart
    cart = session.get('cart', [])

    # Check if the product is already in session cart
    found = False
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            found = True
            break
    
    if not found:
        cart.append({
            "product_id": product[0],
            "product_name": product[1],
            "price": cleaned_price,
            "quantity": quantity
        })

    session['cart'] = cart

    return jsonify({"message": "Item added to cart", "cart": cart})


@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])

    total_price = 0  # Initialize total price

    for item in cart_items:
        price = item.get("price", 0)

        if isinstance(price, str):
            price = float(price.replace("₹", "").replace(",", "").strip())

        item["price"] = float(price)  # Ensure price is always a float

        # ✅ Accumulate total price (fixes total_price = 0 issue)
        total_price += price * item.get("quantity", 1)
        print(f"DEBUG: Total Price Calculated: ₹{total_price}")


    return render_template('cart.html', cart=cart_items, total_price=total_price)


@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    product_id = request.form.get('product_id')
    action = request.form.get('action')  # 'increase' or 'decrease'

    if 'cart' not in session:
        return redirect(url_for('cart'))  # Redirect if no cart

    for item in session['cart']:
        if item['product_id'] == product_id:
            if action == 'increase':
                item['quantity'] += 1  # Increase quantity
            elif action == 'decrease':
                item['quantity'] = max(1, item['quantity'] - 1)  # Decrease but keep minimum 1
            break  # Found the product, no need to continue loop

    session.modified = True  # Mark session as modified to save changes

    return redirect(url_for('cart'))  # Redirect back to cart

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')

    if 'cart' not in session:
        return redirect(url_for('cart'))

    # Remove the product with the matching product_id
    session['cart'] = [item for item in session['cart'] if item['product_id'] != product_id]

    session.modified = True  # Save changes to session

    return redirect(url_for('cart'))


# Close the database connection when the app context is removed
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/check_session')
def check_session():
    return f"User ID: {session.get('user_id', 'Not Logged In')}"

@app.route("/session_test")
def session_test():
    session["test"] = "Hello Flask!"
    return "Session is set!"


@app.route('/checkout', methods=['POST'])
def checkout():

    # Ensure user is logged in
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to checkout.", "error")
        return redirect(url_for("login"))

    # Get form data
    total_price = request.form.get('total_price')
    phone = request.form.get('phone')
    email = request.form.get('email')
    address = request.form.get('address')

    # Check if cart exists
    if "cart" not in session or not session["cart"]:
        flash("Your cart is empty!", "error")
        return redirect(url_for("cart"))

    # Connect to database
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()

    try:
        # ✅ 1. Insert into `orders`
        cursor.execute("""
            INSERT INTO orders (user_id, total_price, phone, email, address) 
            VALUES (?, ?, ?, ?, ?)""",
            (user_id, total_price, phone, email, address)
        )
        order_id = cursor.lastrowid  # Get last inserted order_id

        # ✅ 2. Insert Products into `order_items`
        cursor.execute("""
            SELECT cart.product_id, cart.quantity, products.discounted_price 
            FROM cart 
            JOIN products ON cart.product_id = products.product_id 
            WHERE cart.user_id = ?""", (user_id,))
        
        cart_items = cursor.fetchall()

        for product_id, quantity, price in cart_items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price) 
                VALUES (?, ?, ?, ?)""",
                (order_id, product_id, quantity, price)
            )

        # ✅ 3. Clear cart for user
        cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        flash("An error occurred during checkout!", "error")
        print("Database Error:", e)
        return redirect(url_for("cart"))
    finally:
        conn.close()

    # ✅ Prepare Order Summary for Email
    order_summary = f"""
    Thank you for your order!

    Order Total: ₹{total_price}
    Phone: {phone}
    Address: {address}

    Your order will be processed soon.
    """

    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD") 
    print(EMAIL_PASSWORD)

    # ✅ Send Email Confirmation
    try:
        sender_email = "tervina.samir012@gmail.com"  # Replace with your email
        receiver_email = email
        password = EMAIL_PASSWORD    # Store securely!

        if not password:
            raise ValueError("EMAIL_PASSWORD is missing!")

        print(f"Using password: {password}")  # TEMPORARY DEBUGGING (Remove later!)
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Order Confirmation"
        message["From"] = sender_email
        message["To"] = receiver_email

        part = MIMEText(order_summary, "plain")
        message.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        flash("Order placed successfully! Confirmation sent to your email.", "success")
    except Exception as e:
        print(f"Failed to send email: {e}")
        flash("Order placed, but failed to send confirmation email.", "error")

    return redirect('/')


@app.route("/electronics")
def electronics():
    conn = sqlite3.connect("my_database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get search query from the request parameters
    search_query = request.args.get("search", "").strip().lower()

    # Base SQL query
    sql_query = "SELECT product_id, product_name, actual_price, img_link FROM products WHERE LOWER(category) LIKE 'electronics%'"
    query_params = []

    # If there's a search query, modify the SQL to filter results
    if search_query:
        sql_query += " AND LOWER(product_name) LIKE ?"
        query_params.append(f"%{search_query}%")

    cursor.execute(sql_query, query_params)
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    products = [dict(row) for row in rows]

    print("DEBUG: Products fetched from DB:", products)  # Debugging log

    conn.close()
    return render_template('electronics.html', products=products, search_query=search_query)


@app.route("/computer")
def computer():
    conn = sqlite3.connect("my_database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get search query from the request parameters
    search_query = request.args.get("search", "").strip().lower()

    # Base SQL query
    sql_query = "SELECT product_id, product_name, actual_price, img_link FROM products WHERE LOWER(category) LIKE 'computer%'"
    query_params = []

    # If there's a search query, modify the SQL to filter results
    if search_query:
        sql_query += " AND LOWER(product_name) LIKE ?"
        query_params.append(f"%{search_query}%")

    cursor.execute(sql_query, query_params)
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    products = [dict(row) for row in rows]

    print("DEBUG: Products fetched from DB:", products)  # Debugging log

    conn.close()
    return render_template('electronics.html', products=products, search_query=search_query)


@app.route("/kitchen")
def kitchen():
    conn = sqlite3.connect("my_database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get search query from the request parameters
    search_query = request.args.get("search", "").strip().lower()

    # Base SQL query
    sql_query = "SELECT product_id, product_name, actual_price, img_link FROM products WHERE LOWER(category) LIKE 'home%'"
    query_params = []

    # If there's a search query, modify the SQL to filter results
    if search_query:
        sql_query += " AND LOWER(product_name) LIKE ?"
        query_params.append(f"%{search_query}%")

    cursor.execute(sql_query, query_params)
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    products = [dict(row) for row in rows]

    print("DEBUG: Products fetched from DB:", products)  # Debugging log

    conn.close()
    return render_template('electronics.html', products=products, search_query=search_query)

if __name__ == "__main__":
    app.run(debug=True)
