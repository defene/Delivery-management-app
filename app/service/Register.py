import string
import secrets
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

from app.dtos.RegisterDto import RegisterDTO
from app.repo.UserRepo import UserRepo
from app.repo.VerifyTokenRepo import VerifyTokenRepo
from app.exceptions import ValidationError, TokenError

class RegisterService:
    def __init__(self):
        self.user_repo = UserRepo()
        self.verify_token_repo = VerifyTokenRepo()
    
    def _generate_random_password(self, length=12) -> str:
        """
        Generate a secure random password.

        :param length: Length of the password.
        :return: A securely generated random password string.
        """
        characters = string.ascii_letters + string.digits + string.punctuation
        characters = characters.replace('"', '').replace("'", '').replace('\\', '').replace('/', '')
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    
    def _generate_random_token(self, length=6, expire_minutes: int = 30) -> str:
        """
        Generate a secure random token.

        :param length: Length of the token.
        :return: A securely generated random token string.
        """
        token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
        expires_at = datetime.utcnow() + timedelta(minutes=expire_minutes)
        return token, expires_at
    
    def register_user(self, register_dto: RegisterDTO):
        user_dto = self.user_repo.get_user_by_email(register_dto.email)
        if user_dto is not None and self.user_repo.check_user_role(user_dto.user_id, register_dto.role_name):
            raise ValidationError(f"Username '{register_dto.username}' is already taken.")
        
        if register_dto.role_name == "user":
            token_record = self.verify_token_repo.find_verify_token(register_dto.verify_token)
            if not token_record or token_record.token != register_dto.verify_token:
                # Token not found
                raise TokenError("Invalid token.")

            if token_record.expires_at < datetime.utcnow():
                # Token expired
                raise TokenError("Token expired.")

            # Invalidate the token to prevent reuse
            self.verify_token_repo.invalidate_verify_token(register_dto.verify_token)
        
        if register_dto.role_name == "staff":
            register_dto.password = self._generate_random_password()
        
        if user_dto is not None:
            self.user_repo.add_user_role(register_dto.role_name, user_dto.user_id)
            register_dto.user_id = user_dto.user_id
        else:
            password_hash = generate_password_hash(register_dto.password)
            register_dto.user_id = self.user_repo.create_user(
                                        register_dto.email, 
                                        register_dto.username, 
                                        password_hash,
                                        register_dto.first_name, 
                                        register_dto.last_name, 
                                        register_dto.role_name
                                    )
        return register_dto
    
    def create_verify_token_for_user(self, email: str, expire_minutes=30) -> str:
        """
        1. Find the user by email.
        2. Generate a token and expiration time.
        3. Save the token record in the DB.
        4. Return the token.
        """
        token, expires_at = self._generate_random_token(expire_minutes=expire_minutes)
        self.verify_token_repo.save_verify_token(email, token, expires_at)
        return token