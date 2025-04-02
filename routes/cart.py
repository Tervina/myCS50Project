from flask import Blueprint, jsonify, request, session, render_template, redirect, url_for, flash
import sqlite3

# Create a Blueprint for the cart functionality
cart_bp = Blueprint('cart', __name__)

# Route to view the cart
@cart_bp.route('/cart')
def view_cart():
    cart_items = session.get('cart', [])
    
    total_price = 0  # Initialize total price

    # Calculate the total price and handle pricing in the cart
    for item in cart_items:
        price = item.get("price", 0)

        if isinstance(price, str):
            price = float(price.replace("₹", "").replace(",", "").strip())

        item["price"] = float(price)  # Ensure price is always a float

        # Accumulate total price
        total_price += price * item.get("quantity", 1)

    return render_template('cart.html', cart=cart_items, total_price=total_price)

# Route to add an item to the cart
@cart_bp.route('/add_to_cart', methods=['POST'])
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

    # Fetch product details from database
    product = cursor.execute(
        "SELECT product_id, product_name, actual_price FROM products WHERE product_id = ?",
        (product_id,)
    ).fetchone()

    if not product:
        conn.close()
        return jsonify({"error": "Product not found"}), 404

    # Clean the price (remove ₹ symbol, commas, and ensure it's numeric)
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

# Route to update quantity in the cart
@cart_bp.route('/update_quantity', methods=['POST'])
def update_quantity():
    product_id = request.form.get('product_id')
    action = request.form.get('action')  # 'increase' or 'decrease'

    if 'cart' not in session:
        return redirect(url_for('cart.view_cart'))  # Redirect if no cart

    for item in session['cart']:
        if item['product_id'] == product_id:
            if action == 'increase':
                item['quantity'] += 1  # Increase quantity
            elif action == 'decrease':
                item['quantity'] = max(1, item['quantity'] - 1)  # Decrease but keep minimum 1
            break  # Found the product, no need to continue loop

    session.modified = True  # Mark session as modified to save changes

    return redirect(url_for('cart.view_cart'))  # Redirect back to cart

# Route to remove an item from the cart
@cart_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')

    if 'cart' not in session:
        return redirect(url_for('cart.view_cart'))  # Redirect if no cart

    # Remove the product with the matching product_id
    session['cart'] = [item for item in session['cart'] if item['product_id'] != product_id]

    session.modified = True  # Save changes to session

    return redirect(url_for('cart.view_cart'))  # Redirect back to cart
