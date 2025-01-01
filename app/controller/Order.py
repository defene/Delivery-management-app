from flask import Blueprint, jsonify, request
from app.service.Order import OrderService
from app.models.OrderModel import OrderModel
from app.decorators import token_required, roles_required 

order = Blueprint('order', __name__, url_prefix='/order')

@order.route('/create', methods=['POST'])
@token_required
@roles_required('user')
def create_order():
    data = request.json
    
