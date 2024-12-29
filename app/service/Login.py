from werkzeug.security import check_password_hash

from app.dtos.LoginDto import LoginDto
from app.utils.token_utils import generate_jwt
from app.repo.UserRepo import UserRepo
from app.exceptions import AuthenticationError

EXPIRES_IN = 3600

class LoginService:
    def __init__(self):
        self.user_repo = UserRepo()
    
    def authenticate_user(self, login_dto: LoginDto):
        user_dto = self.user_repo.get_user_by_email(login_dto.email)
        if user_dto is None:
            raise AuthenticationError("Invalid email or password.")
        
        password_hash = user_dto.password_hash
        user_id = user_dto.user_id
        
        print(password_hash)
        
        if not password_hash or not check_password_hash(password_hash, login_dto.password):
            raise AuthenticationError("Invalid email or password.")

        if not self.user_repo.check_user_role(user_dto.user_id, login_dto.role_name):
            raise AuthenticationError(f"You don't have permission to access this resource.")
        
        token = generate_jwt(user_id, login_dto.role_name, expires_in=EXPIRES_IN)

        return {
            "message": "Successfully authenticated user.",
            "token": token,
            "expires_in": EXPIRES_IN
        }