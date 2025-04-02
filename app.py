from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from routes.auth import auth_bp
from routes.product import product_bp
from routes.cart import cart_bp
from routes.order import checkout_bp
from config import Config
from routes.category import category_bp



app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = '30dc62dc9f43c1410154a6cc394fd3f48bc6fb65cba19c7b8a876376ec84b2bf';


# Enable CSRF protection
csrf = CSRFProtect(app)

# Initialize Flask session management
Session(app)

# Register blueprints (modular routes)
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
# app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(checkout_bp)
# app.register_blueprint(main_bp)
app.register_blueprint(category_bp)

if __name__ == "__main__":
    app.run(debug=True)
