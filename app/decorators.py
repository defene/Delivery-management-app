from functools import wraps
from flask import request, jsonify
from app.utils.token_utils import decode_jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Missing Authorization header"}), 401
        
        try:
            bearer, token = auth_header.split()
            if bearer.lower() != "bearer":
                return jsonify({"message": "Invalid Authorization header format"}), 401
        except ValueError:
            return jsonify({"message": "Invalid Authorization header format"}), 401
        
        try:
            user_info = decode_jwt(token)
        except Exception as e:
            return jsonify({"message": "Invalid or expired token"}), 401
        print(user_info)
        if not user_info:
            return jsonify({"message": "Invalid or expired token"}), 401
        
        # Attach user_info to the request context if needed
        request.user = user_info
        return f(*args, **kwargs)
    
    return decorated

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_info = getattr(request, 'user', None)
            if not user_info or user_info.get("role_name") not in roles:
                return jsonify({"message": "Unauthorized"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator