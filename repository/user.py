
from repository.db import get_db_connection

def create_user(user_name, email, password):
    """Create a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO user (user_name, email, password) VALUES (?, ?, ?)",
        (user_name, email, password)
    )
    
    conn.commit()
    conn.close()
    return True

def get_user_by_username(user_name):
    """Get user by username"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM user WHERE user_name = ?", (user_name,))
    user = cursor.fetchone()
    
    conn.close()
    return user

def get_user_by_email(email):
    """Get user by email"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    conn.close()
    return user

def update_password(email, new_password):
    """Update user password"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE user SET password = ? WHERE email = ?", (new_password, email))
    
    conn.commit()
    conn.close()
    return cursor.rowcount > 0