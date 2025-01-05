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
        
@order_bp.route('/delete/<int:order_id>', methods=['DELETE'])
@token_required
@roles_required('user')
def delete_order(order_id):
    """
    Deletes an order by its ID.
    """
    try:
        order_service.delete_order(order_id)
        return jsonify({"message": f"Order with ID {order_id} has been deleted successfully."}), 200
    except Exception as e:
        return handle_exception(e)
    
@order_bp.route('/orders', methods=['GET'])
@token_required
@roles_required('user')
def get_user_orders():
    """
    API endpoint to fetch all orders for the authenticated user.

    :return: A JSON response with the list of orders.
    """
    try:
        user_id = int(request.user["sub"])  # Extract user ID from bearer token
        orders = order_service.get_user_orders(user_id)
        orders_data = [
            {
                "order_id": order.order_id,
                "user_id": order.user_id,
                "station_id": order.station_id,
                "delivery_src_address_id": order.delivery_src_address_id,
                "delivery_dst_address_id": order.delivery_dst_address_id,
                "created_at": order.created_at,
                "updated_at": order.updated_at,
                "expected_at": order.expected_at,
                "total_price": order.total_price,
                "order_status": order.order_status,
                "delivery_method": order.delivery_method,
                "category": order.category,
                "payload": order.payload,
                "package_size": order.package_size,
                "notes": order.notes,
            }
            for order in orders
        ]
        return jsonify(orders_data), 200
    except Exception as e:
        return handle_exception(e)