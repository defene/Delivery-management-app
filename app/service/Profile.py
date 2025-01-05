import pymysql

from app.BaseService import BaseService
from app.repo.UserRepo import UserRepo
from app.models.UserModel import UserDto, UserWithoutPasswordDto
from config import Config
from werkzeug.security import generate_password_hash


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

    # def check_user_password(self,user_id):
    #     return

    def update_user_by_id_no_password(self, response_data):
        if self.get_user_by_id(response_data['user_id']) is None:
            return 0
        user_dto = UserDto(**response_data)
        return UserRepo.update_user_by_id_no_password(self.conn, user_dto)

    # 核对密码
    # 返回原密码输入是否正确
    def check_user_password(self, user_id, old_password):
        # 找不到该用户
        if self.get_user_by_id(user_id) is None:
            return 0

        # 该用户原密码输入错误
        if UserRepo.check_user_password(self.conn, user_id, old_password):
            return 1
        else:
            return 2

    def update_password(self, user_id, new_password):
        new_password_hash = generate_password_hash(new_password)

        return UserRepo.update_user_password(self.conn, user_id, new_password_hash)
