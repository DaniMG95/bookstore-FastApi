JWT_SECRET_KEY = "edba2905819e783f038f495e35b96fb44a5708a372498ae6678916c4c03f428f"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 60 * 24 * 5

DESCRIPTION_JWT_TOKEN = "It checks username and password if they are true, it return JWT Token."
SUMMARY_JWT_TOKEN = "It returns JWT token."

DB_HOST = "localhost"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_DATABASE = "bookstore"
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
REDIS_URL = f"redis://localhost"
YOUR_CLIENT_API_KEY = "08a293690f0c146301434b1f31928287"

UPLOAD_PHOTO_URL = f"https://api.imgbb.com/1/upload?expiration=600&key={YOUR_CLIENT_API_KEY}"

TESTING = True
LOAD_TESTING = True

DB_HOST_TEST = "localhost"
DB_USER_TEST = "test"
DB_PASSWORD_TEST = "test"
DB_DATABASE_TEST = "bookstore_test"
DB_URL_TEST = f"postgresql://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}:5433/{DB_DATABASE_TEST}"
