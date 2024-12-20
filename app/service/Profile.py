import pymysql

from app.BaseService import BaseService
from app.repo.user import UserRepo
from app.models.user import UserDto
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
        return UserDto(*user)
