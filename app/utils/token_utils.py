import jwt
import uuid
from datetime import datetime, timedelta, timezone
from flask import current_app
from typing import Optional, Dict

def generate_jwt(user_id: int, role_name: str, expires_in: int = 36000) -> str:
    """
    Generate and return a JWT token as a string.
    
    :param user_id: Unique identifier for the user
    :param role_name: Role name of the user
    :param expires_in: Token expiration time in seconds (default is 36000 seconds)
    :return: JWT token string
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),  # Subject of the token
        "role_name": role_name,   # User's role ID
        "iat": int(now.timestamp()),  # Issued at time (as a Unix timestamp)
        "exp": int((now + timedelta(seconds=expires_in)).timestamp())  # Expiration time (as a Unix timestamp)
    }

    # Encode the JWT with the specified algorithm
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    return token

def decode_jwt(token: str) -> Optional[Dict]:
    try:
        payload = jwt.decode(
            token, 
            current_app.config["SECRET_KEY"], 
            algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        # Token has expired
        raise jwt.ExpiredSignatureError("Token has expired")
    except jwt.InvalidTokenError:
        # Token is invalid for other reasons
        raise jwt.InvalidTokenError("Invalid token")
    
    return payload


def generate_reset_token(expire_minutes: int = 30):
    """
    Generate a random token (UUID) and calculate an expiration time.
    """
    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(minutes=expire_minutes)
    return token, expires_at
