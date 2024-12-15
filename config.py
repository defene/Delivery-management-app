class Config:
    SECRET_KEY = 'your_secret_key'   # Required to avoid Flask warnings, used for securely signing session cookies
    DEBUG = True                    # Enable debug mode for development
    MYSQL_HOST = 'localhost'        # Database host
    MYSQL_PORT = 3306               # Database port
    MYSQL_USER = 'root'             # Database user
    MYSQL_PASSWORD = '123456'       # Database password
    MYSQL_DB = 'Delivery'           # Target database name