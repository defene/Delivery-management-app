from flask import Blueprint, jsonify, request
from app.service.Profile import ProfileService
from app.models.UserModel import UserDto

profile = Blueprint('profile', __name__, url_prefix='/profile')

@profile.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    profile_service = ProfileService()
    user_dto = profile_service.get_user_by_id(id)
    print(user_dto)
    if not user_dto:
        return jsonify({'detail': 'User not found'}), 404
    else:
        return jsonify(user_dto.__dict__)


@profile.route('/<int:id>', methods=['POST'])
def update_user_by_id_no_password(id):
    profile_service = ProfileService()
    data = request.get_json()
    data['user_id'] = id

    ret = profile_service.update_user_by_id_no_password(data)
    if ret < 1:
        return jsonify({'detail': 'User not found'}), 404
    else:
        return jsonify({'message': 'User updated successfully'}), 200
    