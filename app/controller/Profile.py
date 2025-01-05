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


# 修改不包含密码的个人信息
@profile.route('/<int:id>', methods=['POST'])
def update_user_by_id_no_password(id):
    profile_service = ProfileService()
    data = request.get_json()
    print(data)
    data['user_id'] = id

    ret = profile_service.update_user_by_id_no_password(data)
    if ret < 1:
        return jsonify({'detail': 'User not found'}), 404
    else:
        return jsonify({'message': 'User updated successfully'}), 200


# 修改密码
@profile.route('/password/<int:user_id>', methods=['POST'])
def update_user_password(user_id):
    profile_service = ProfileService()
    old_password = "123123"
    new_password = "123123"

    ret = profile_service.check_user_password(user_id, old_password)
    if ret == 0:
        return jsonify({'detail': 'User not found'}), 404
    if ret == 1:
        return jsonify({'detail': 'Wrong old password'}), 404

    # 正确输入，修改密码
    print("right old password")
    profile_service.update_password(user_id, new_password)
    return jsonify({'message': 'Password updated successfully'}), 200
