from .Profile import profile
from .User import auth_bp
from .Address import address_bp
from .Order import order_bp
from .Station import station_controller

blueprints = [profile, auth_bp, address_bp, order_bp, station_controller]
