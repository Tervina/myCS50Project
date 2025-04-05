import random
import requests
from repository.db import get_db_connection
from config import Config

def is_valid_image_url(url):
    """Check if an image URL is reachable (HTTP status 200)"""
    try:
        response = requests.head(url, timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_product_by_id(product_id):
    """Get a product by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT product_id, product_name, category, discounted_price, actual_price, "
        "discount_percentage, rating, img_link, about_product FROM products WHERE product_id = ?",
        (product_id,)
    )
    
    product = cursor.fetchone()
    conn.close()
    
    return product

def get_random_products(limit=10):
    """Get random products from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT product_id, product_name, category, discounted_price, actual_price, "
        "discount_percentage, rating, img_link FROM products"
    )
    print(f"DEBUG: PLACEHOLDER_IMAGE = {getattr(Config, 'PLACEHOLDER_IMAGE', 'NOT FOUND')}")

    # Fetch all products
    all_products = cursor.fetchall()
    print(f"DEBUG: Total products fetched: {len(all_products)}")
    
    # Get column names
    columns = [column[0] for column in cursor.description]
    
    # Convert rows to dictionaries
    products_list = []
    for row in all_products:
        product_dict = {}
        for i, column in enumerate(columns):
            product_dict[column] = row[i]
        products_list.append(product_dict)
    
    conn.close()

    if not products_list:
        return []

    # Select random products
    random_products = random.sample(products_list, min(limit, len(products_list)))
    print(f"DEBUG: Selected {len(random_products)} random products")

   
    # Check the validity of the image URLs
    for product in random_products:
        img_link = product['img_link']
        
        # If the image URL is not valid, replace it with the placeholder
        if not is_valid_image_url(img_link):
            product['img_link'] = Config.PLACEHOLDER_IMAGE

    return random_products

def get_products_by_category(category, search_query=None):
    """Get products by category with optional search filtering"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Base SQL query
    sql_query = "SELECT product_id, product_name, actual_price, img_link FROM products WHERE LOWER(category) LIKE ?"
    query_params = [f"{category}%"]
    
    # If there's a search query, add it to the filter
    if search_query:
        sql_query += " AND LOWER(product_name) LIKE ?"
        query_params.append(f"%{search_query}%")
    
    cursor.execute(sql_query, query_params)
    rows = cursor.fetchall()
    
    products = [dict(row) for row in rows]
    conn.close()
    
    return products