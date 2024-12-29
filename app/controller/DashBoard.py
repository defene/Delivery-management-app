from flask import Blueprint, jsonify, request
from app.service.Profile import ProfileService
from app.models.UserModel import UserDto

profile = Blueprint('profile', __name__, url_prefix='/dashboard')

