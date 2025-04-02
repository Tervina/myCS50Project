from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask import Blueprint, request, redirect, url_for, session, flash
import sqlite3
from utils.email import send_order_confirmation_email
import os

checkout_bp = Blueprint('order', __name__)


@checkout_bp.route('/checkout', methods=['POST'])
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

