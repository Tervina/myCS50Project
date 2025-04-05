import re
from repository.db import get_db_connection

def clean_price(price_str):
    """Clean price string by removing currency symbols and commas"""
    if isinstance(price_str, str):
        clean = re.sub(r'[^\d.]', '', price_str)
        return float(clean) if clean else 0.0
    return float(price_str) if price_str else 0.0

def add_to_cart(user_id, product_id, quantity=1):
    """Add a product to the cart or update quantity if it already exists"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the product exists
    cursor.execute(
        "SELECT product_id, product_name, actual_price FROM products WHERE product_id = ?",
        (product_id,)
    )
    product = cursor.fetchone()
    
    if not product:
        conn.close()
        return None, "Product not found"
    
    # Clean price
    cleaned_price = clean_price(product['actual_price'])
    
    # Check if product is already in cart
    cursor.execute(
        "SELECT quantity FROM cart WHERE user_id = ? AND product_id = ?", 
        (user_id, product_id)
    )
    existing_product = cursor.fetchone()
    
    if existing_product:
        # Update quantity
        new_quantity = existing_product['quantity'] + quantity
        cursor.execute(
            "UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?",
            (new_quantity, user_id, product_id)
        )
    else:
        # Add new item
        cursor.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
            (user_id, product_id, quantity)
        )
    
    conn.commit()
    conn.close()
    
    return {
        "product_id": product['product_id'],
        "product_name": product['product_name'],
        "price": cleaned_price,
        "quantity": quantity
    }, "Item added to cart"

def get_cart_items(user_id):
    """Get all items in a user's cart"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT c.product_id, p.product_name, p.actual_price, c.quantity "
        "FROM cart c JOIN products p ON c.product_id = p.product_id "
        "WHERE c.user_id = ?",
        (user_id,)
    )
    
    items = cursor.fetchall()
    conn.close()
    
    # Clean prices
    cart_items = []
    for item in items:
        cleaned_price = clean_price(item['actual_price'])
        
        cart_items.append({
            "product_id": item['product_id'],
            "product_name": item['product_name'],
            "price": cleaned_price,
            "quantity": item['quantity']
        })
    
    return cart_items

def update_cart_quantity(user_id, product_id, action):
    """Update quantity of an item in the cart"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT quantity FROM cart WHERE user_id = ? AND product_id = ?", 
                  (user_id, product_id))
    item = cursor.fetchone()
    
    if not item:
        conn.close()
        return False
    
    current_quantity = item['quantity']
    new_quantity = current_quantity + 1 if action == 'increase' else max(1, current_quantity - 1)
    
    cursor.execute("UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?",
                  (new_quantity, user_id, product_id))
    
    conn.commit()
    conn.close()
    return True

def remove_from_cart(user_id, product_id):
    """Remove an item from the cart"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM cart WHERE user_id = ? AND product_id = ?",
                  (user_id, product_id))
    
    conn.commit()
    conn.close()
    return True

def clear_cart(user_id):
    """Remove all items from a user's cart"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    
    conn.commit()
    conn.close()
    return True