import json
from flask import Blueprint, jsonify, request
from app.service.Order import OrderService
from app.dtos.OrderDto import OrderDTO
from app.decorators import token_required, roles_required 
from app.utils.validation import Validator
from app.exceptions import handle_exception

order_bp = Blueprint('order', __name__, url_prefix='/order')
order_service = OrderService()

@order_bp.route('/create', methods=['POST'])
@token_required
@roles_required('user')
def create_order():
    try:
        data = request.json
        
        required_fields = ["station_id",
            "source_address_id", 
            "dest_address_id", 
            "package_size", 
            "package_weight", 
            "delivery_method",
            "route"
        ]
        
        Validator.validate_required_fields(data, required_fields)
        if isinstance(data.get('route'), str):
            try:
                data['route'] = json.loads(data['route'])
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format for 'route'")
        
        if isinstance(data.get('package_size'), str):
            try:
                data['package_size'] = json.loads(data['package_size'])
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format for 'package_size'")
        
        order_dto = OrderDTO(
            station_id=data['station_id'],
            user_id=request.user["sub"],
            source_address_id=data['source_address_id'],
            dest_address_id=data['dest_address_id'],
            delivery_method=data['delivery_method'],
            package_size_length=data['package_size']['length'],
            package_size_width=data['package_size']['width'],
            package_size_height=data['package_size']['height'],
            package_weight=data['package_weight'],
            total_price=data['total_price'],
            category=data.get('category'),
            distance=data['route']['distance'],
            duration=data['route']['duration'],
            notes=data.get('notes')
        )
        
        response = order_service.create_order(order_dto)
        return jsonify(response), 201
    except Exception as e:
        return handle_exception(e)
        