from flask import g, current_app
from werkzeug.security import generate_password_hash
import pymysql

def create_database(host, port, user, password, database_name):
    """
    Check if the database exists, and create it if it does not.
    """
    db = None
    try:
        # Connect to MySQL server without specifying a database
        db = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        with db.cursor() as cursor:
            # Create database if it doesn't exist
            print(f"Creating database: {database_name}")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`;")
        db.commit()
        print("Database creation completed successfully!")
    except pymysql.MySQLError as e:
        print(f"Error during database creation: {e}")
    finally:
        if db is not None:
            db.close()

def init_db(app):
    """
    Initialize the database connection for the Flask application.
    """
    @app.before_request
    def connect_db():
        # Establish a database connection before handling each request
        if 'db' not in g:
            g.db = pymysql.connect(
                host=app.config['MYSQL_HOST'],
                port=app.config['MYSQL_PORT'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PASSWORD'],
                db=app.config['MYSQL_DB'],
                cursorclass=pymysql.cursors.DictCursor
            )

    @app.teardown_request
    def close_db(exception=None):
        # Close the database connection after handling each request
        db = g.pop('db', None)
        if db is not None:
            db.close()

def get_db_connection():
    """
    Retrieve the database connection from the Flask global object.
    """
    return g.db

def import_sql_file():
    """
    Import and execute the SQL file to initialize database schema and data.
    """
    try:
        db = pymysql.connect(
            host=current_app.config['MYSQL_HOST'],
            port=current_app.config['MYSQL_PORT'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        with db.cursor() as cursor:
            # Read and execute SQL file
            with open('init_db.sql', 'r') as f:
                sql = f.read()
            for statement in sql.split(';'):
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except pymysql.MySQLError as e:
                        print(f"Error executing SQL: {statement}\n{e}")
            db.commit()
    finally:
        db.close()

def hash_and_update_passwords():
    """
    Connect to the MySQL database, retrieve plain text passwords,
    hash them using Werkzeug's generate_password_hash, and update the database.
    """
    try:
        # Establish a database connection
        db = pymysql.connect(
            host=current_app.config['MYSQL_HOST'],
            port=current_app.config['MYSQL_PORT'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = db.cursor()
        
        # Fetch all users and their plain text passwords
        cursor.execute("SELECT user_id, password_hash FROM User")
        users = cursor.fetchall()
        
        # Iterate over each user to hash passwords and update the database
        for user_name, plain_password in users:
            hashed_password = generate_password_hash(plain_password)
            
            # Update the database with the hashed password
            cursor.execute(
                "UPDATE User SET password_hash = %s WHERE user_id = %s",
                (hashed_password, user_name)
            )
        
        # Commit changes to the database
        db.commit()
        print("Password hashing and update completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()