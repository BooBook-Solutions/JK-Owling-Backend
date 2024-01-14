import os

# Database
MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/')
POSTGRES_URL = os.getenv('POSTGRES_URL', 'postgresql://postgres:password@localhost:5432/jkowling')
DB_TYPE = os.getenv('DB_TYPE', 'postgresql')  # postgresql or mongodb

# Authentication
HASH_SECRET_KEY = os.getenv('HASH_SECRET_KEY', '')
HASH_ALGORITHM = os.getenv('HASH_ALGORITHM', 'HS256')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')

# Settings
ADMIN_ROLE = os.getenv('ADMIN_ROLE', 'admin')
USER_ROLE = os.getenv('USER_ROLE', 'user')

# Frontend
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

# Apis
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '')
AMAZON_EXTRACTOR_URL = os.getenv('AMAZON_EXTRACTOR_URL', '')
AMAZON_EXTRACTOR_KEY = os.getenv('AMAZON_EXTRACTOR_KEY', '')
BOOK_INFO_URL = os.getenv('BOOK_INFO_URL', '')

