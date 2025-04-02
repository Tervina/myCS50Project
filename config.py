import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_default_key")
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_SECURE = False  # Set to True in production
    PLACEHOLDER_IMAGE = "/static/images/out_of_stock.png"