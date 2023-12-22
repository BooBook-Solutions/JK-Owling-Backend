import os

# Database connection URL
MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/')

# JWT secret key
HASH_SECRET_KEY = os.getenv('HASH_SECRET_KEY', 'secret-key')

