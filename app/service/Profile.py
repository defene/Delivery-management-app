import pymysql

from app.BaseService import BaseService
from app.repo.UserRepo import UserRepo
from app.models.UserModel import UserDto,UserWithoutPasswordDto
from config import Config

class ProfileService(BaseService):
    def __init__(self):
        super().__init__()
        self.conn = pymysql.connect(
            host=Config.MYSQL_HOST,
            port=int(Config.MYSQL_PORT),
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            db=Config.MYSQL_DB,
        )

    def get_user_by_id(self, user_id):
        user = UserRepo.get_user_by_id(self.conn, user_id)
        print(user)
        return UserWithoutPasswordDto(user) if user else None
    
    def update_user_by_id_no_password(self, response_data):
        if self.get_user_by_id(response_data['user_id']) is None:
            return 0
        user_dto = UserDto(**response_data)
        return UserRepo.update_user_by_id_no_password(self.conn, user_dto)
