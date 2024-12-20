# Delivery-management-app

We are a logistics company with a service that uses ground-based robotic assistants and drones to deliver small and medium-sized items to users within the city of San Francisco, where we have a total of 3 distribution stations. Our interaction design requirements are web application

Please put a file named `config.py` under the root of the project. This file contains some credential information, such as database configuration.

**config.py demo:**

```python
class Config:
    SECRET_KEY = 'your_secret_key'   # Required to avoid Flask warnings, used for securely signing session cookies
    DEBUG = True                    # Enable debug mode for development
    MYSQL_HOST = 'localhost'        # Database host
    MYSQL_PORT = 3306               # Database port
    MYSQL_USER = 'root'             # Database user
    MYSQL_PASSWORD = '123456'       # Database password
    MYSQL_DB = 'Delivery'           # Target database name
```
