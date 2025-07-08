import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
          'mysql+pymysql://bismark_support:StrongPassword123!@localhost/bismark_support_db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

    WPP_API_BASE_URL = os.environ.get("WPP_API_BASE_URL") or "http://localhost:21465/api"
    WPP_SESSION_NAME = os.environ.get("WPP_SESSION_NAME") or "mySession"
    WPP_SESSION_TOKEN = os.environ.get("WPP_SESSION_TOKEN") or "$2b$10$8sdQhP86c6QsfOCI3set4ugI2gadgnHB6KzD0MSIGt6Z5FGVlpRXO"
