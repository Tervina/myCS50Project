import sqlite3
from config import Config
import os

# def get_db_connection():
#     """Create a database connection"""
#     conn = sqlite3.connect("/mnt/e/CS50/finalProject/my_database.db")
#     conn.row_factory = sqlite3.Row  # Return rows as dictionaries
#     return conn
def get_db_connection():
    """Create a database connection"""
    db_path = "/mnt/e/CS50/finalProject/my_database.db"
    print(f"DEBUG: Connecting to database at: {os.path.abspath(db_path)}")
    print(f"DEBUG: Database file exists: {os.path.exists(db_path)}")
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        print("DEBUG: Connection successful!")  # ✅ Debugging print
        print(Config.PLACEHOLDER_IMAGE)

        return conn
    except sqlite3.Error as e:
        print(f"ERROR: Database connection failed: {e}")  # ✅ Error handling
        return None
