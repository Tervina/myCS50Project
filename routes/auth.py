from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from utils.email import send_password_reset_email
from repository.user import create_user, get_user_by_username, get_user_by_email, update_password
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, flash, render_template, session, redirect, url_for
from repository.product import get_random_products
from config import Config
# from flask_wtf.csrf import csrf_exempt  # Import the decorator directly
from flask_wtf.csrf import validate_csrf
from wtforms.csrf.core import ValidationError

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/home')
def home():
    if "user_id" not in session:  # If user is not logged in
        return redirect(url_for("login"))  # Redirect to login
     
    # Fetch random products using the existing function
    products = get_random_products()  # This returns a list of dictionaries

    # Debug the products variable
    print(f"DEBUG: Products before template: {products}")
    print(f"DEBUG: Type of products: {type(products)}")
    print(f"DEBUG: Length of products: {len(products) if products else 0}")
    print(Config.PLACEHOLDER_IMAGE)

    print(f"Fetched products: {products}")


    if not products:  # Handle the case if no products are returned
        flash("No products found.")

    # Force a simple list of products for testing
    if not products:
        products = [
            {"product_id": 1, "product_name": "Test Product", "discounted_price": 99.99, 
             "rating": 4.5, "img_link": "/static/images/out_of_stock.png"}
        ]
        print("DEBUG: Using test products")

    return render_template("home.html", products=products)


@auth_bp.route("/")
def index():
    if "user" in session:  # If user is already logged in
        return redirect(url_for("auth.home"))
    
    return redirect(url_for("auth.login"))


# @auth_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'GET':
#         return render_template("register.html")

#     try:
#         print("Headers:", request.headers)  
#         print("Raw Data Received:", request.data)  

#         # More explicit check for JSON content type
#         if not request.is_json:
#             print("Request is not JSON")
#             return jsonify({"error": "Request must be JSON"}), 400

#         data = request.get_json()
#         print("Parsed data:", data)  # Add this log
        
#         if not data:
#             return jsonify({"error": "Invalid or missing JSON data"}), 400

#         user_name = data.get('user_name')
#         email = data.get('email')
#         password = data.get('password')

#         print(f"Processing: {user_name}, {email}, {password[:2]}***")  # Log processing

#         if not user_name or not email or not password:
#             return jsonify({"error": "Missing required fields"}), 400

#         conn = sqlite3.connect("my_database.db")
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO user (user_name, email, password) VALUES (?, ?, ?)",
#                       (user_name, email, password))
#         conn.commit()
#         conn.close()

#         print("User registered successfully")
#         return jsonify({"message": "User registered successfully!"}), 201

#     except Exception as e:
#         print(f"Exception: {str(e)}")
#         return jsonify({"error": str(e)}), 400

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    try:
        print("Headers:", request.headers)
        print("Raw Data Received:", request.data)

        if not request.is_json:
            print("Request is not JSON")
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        print("Parsed data:", data)

        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        user_name = data.get('user_name')
        email = data.get('email')
        password = data.get('password')

        print(f"Processing: {user_name}, {email}, {password[:2]}***")

        if not user_name or not email or not password:
            return jsonify({"error": "Missing required fields"}), 400

        # Use context manager with timeout to avoid locking issues
        with sqlite3.connect("my_database.db", timeout=10) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user (user_name, email, password) VALUES (?, ?, ?)",
                           (user_name, email, password))
            conn.commit()

        print("User registered successfully")
        return jsonify({"message": "User registered successfully!"}), 201

    except sqlite3.OperationalError as e:
        if "locked" in str(e):
            print("⚠️ Database is locked, try again later.")
            return jsonify({"error": "Database is busy, please try again shortly."}), 503
        print(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        print(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 400
    
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if "user" in session:  # Check if user is already logged in
        return redirect(url_for("home.html"))  # Redirect to home
    
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
                    return jsonify({"message": "Login successful", "redirect": "auth.home"}), 200
                else:
                    return jsonify({"error": "Invalid username or password"}), 401
            else:
                return jsonify({"error":"user not found"}),404
    except Exception as e:
        print("Login error:", str(e))  # Debugging: Print error
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/logout')
def logout():
    session.pop("user_id", None)
    session.clear()  # ✅ Clear all session data  # Remove user session
    return redirect(url_for("auth.login"))
@auth_bp.route('/forget-pass', methods=['GET', 'POST'])
def forget():
    if request.method == 'GET':
        return render_template("forget-pass.html")
    try:
        print("Request Headers:", request.headers)  # Log request headers
        print("Request Body:", request.data)  # Log request body
        
        data = request.get_json(silent=True)
        if not data:
            print("No JSON data found in request.")
            return jsonify({"error": "Invalid or missing JSON in request"}), 400
        
        email = data.get('email', '').strip()
        new_password = data.get('new_password', '').strip()

        if not email or not new_password:
            return jsonify({"error": "Please provide both email and new password"}), 400
        
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "Email not found"}), 404

        cursor.execute("UPDATE user SET password = ? WHERE email = ?", (new_password, email))

        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            return jsonify({"error": "Email not found"}), 404
        
        return jsonify({"message": "Password updated successfully!"}), 200

    except Exception as e:
        print("❌ Exception occurred:", str(e))
        return jsonify({"error": str(e)}), 400
