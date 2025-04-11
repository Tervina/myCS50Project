from flask import Flask
# from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from routes.auth import auth_bp
from routes.product import product_bp
from routes.cart import cart_bp
from routes.order import checkout_bp
from config import Config
from routes.category import category_bp





app = Flask(__name__)
app.config.from_object(Config)
app.config['JSON_AS_ASCII'] = False  # Properly handle non-ASCII characters
# app.secret_key = '30dc62dc9f43c1410154a6cc394fd3f48bc6fb65cba19c7b8a876376ec84b2bf';

app.config['SECRET_KEY'] = '30dc62dc9f43c1410154a6cc394fd3f48bc6fb65cba19c7b8a876376ec84b2bf'
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection



# Initialize Flask session management
Session(app)

# Register blueprints (modular routes)
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(checkout_bp)
app.register_blueprint(category_bp)

if __name__ == "__main__":
    app.run(debug=True)

app.config['JSON_AS_ASCII'] = False


#from flask import Flask, request
# from flask_session import Session
# from extensions import csrf  # Import from extensions instead
# from config import Config
# from flask_wtf.csrf import CSRFProtect, generate_csrf
# from flask import request, jsonify
# from flask_wtf.csrf import validate_csrf
# from wtforms.csrf.core import ValidationError
# app = Flask(__name__)
# app.config.from_object(Config)
# app.secret_key = '30dc62dc9f43c1410154a6cc394fd3f48bc6fb65cba19c7b8a876376ec84b2bf';

# # Initialize CSRF with the app
# # csrf.init_app(app)

# # Make sure the CSRF token is available in the headers for JSON requests
# # @app.after_request
# # def add_csrf_token(response):
# #     response.set_cookie('csrf_token', generate_csrf())
#     # return response

# # @app.route('/api/data', methods=['POST'])
# # def api_data():
# #     token = request.headers.get("X-CSRFToken")
# #     try:
# #         validate_csrf(token)
# #     except ValidationError:
# #         return jsonify({"error": "Invalid or missing CSRF token"}), 400

# #     # Proceed with logic
# #     return jsonify({"message": "Success!"})
# # # Initialize Flask session management
# Session(app)

# # Import routes after creating app to avoid circular imports
# from routes.auth import auth_bp
# from routes.product import product_bp
# from routes.cart import cart_bp
# from routes.order import checkout_bp
# from routes.category import category_bp

# # Register blueprints (modular routes)
# app.register_blueprint(auth_bp)
# app.register_blueprint(product_bp)
# app.register_blueprint(cart_bp)
# app.register_blueprint(checkout_bp)
# app.register_blueprint(category_bp)

# if __name__ == "__main__":
#     app.run(debug=True)

# app.config['JSON_AS_ASCII'] = False