from .Profile import profile
from .User import auth_bp
from .Address import address_bp

blueprints = [profile, auth_bp, address_bp]
