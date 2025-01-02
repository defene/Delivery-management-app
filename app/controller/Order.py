from flask import Blueprint, jsonify, request
from app.service.Order import OrderService
from app.dtos.OrderDto import OrderDTO
from app.decorators import token_required, roles_required 
from app.utils.validation import Validator
from app.exceptions import handle_exception

order = Blueprint('order', __name__, url_prefix='/order')

@order.route('/create', methods=['POST'])
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
        Validator.validate_json_field(data.get('route'), 'route')
        Validator.validate_json_field(data.get('package_size'), 'package_size')
        
        order_dto = OrderDTO(
            station_id=data['station_id'],
            user_id=request.user["sub"],
            source_address_id=data['source_address_id'],
            dest_address_id=data['dest_address_id'],
            delivery_method=data['delivery_method'],
            package_size_length=data['package_size'][0],
            package_size_width=data['package_size'][1],
            package_size_height=data['package_size'][2],
            package_weight=data['package_weight'],
            category=data.get('category'),
            distance=data['route'][0],
            duration=data['route'][1],
            notes=data.get('notes')
        )
        
        response = OrderService.create_order(order_dto)
        return jsonify(response), 201
    except Exception as e:
        return handle_exception(e)
        