from flask import Blueprint, jsonify, request
from app.decorators import token_required
from app.service.Address import AddressService
from app.models.AddressInfoModel import AddressInfoDto


address_bp = Blueprint('address', __name__)

@address_bp.route('/address', methods=['GET'])
@token_required
def get_address_info():
    data = request.user
    user_id = data['sub']
    address_service = AddressService()
    address_info = address_service.find_address_info(user_id)

    return jsonify(address_info), 200


@address_bp.route('/address', methods=['POST'])
@token_required
def save_address_info():
    data = request.get_json()
    user_id = request.user['sub']
    address_service = AddressService()
    address_service.save_address_info(user_id, data)
    return jsonify({'message': 'Address saved successfully'}), 200
