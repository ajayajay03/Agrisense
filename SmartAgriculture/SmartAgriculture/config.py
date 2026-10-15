import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Runtime configuration sourced from .env, never hard-coded secrets."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-development-key')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'smart_agriculture')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    WTF_CSRF_TIME_LIMIT = 3600
