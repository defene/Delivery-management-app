from flask import Blueprint, jsonify
from app.service.Profile import ProfileService

profile = Blueprint('profile', __name__, url_prefix='/profile')

@profile.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    profile_service = ProfileService()
    user_dto = profile_service.get_user_by_id(id)
    return jsonify(user_dto.__dict__)
