import string
import secrets
from werkzeug.security import generate_password_hash

from app.dtos.RegisterDto import RegisterDTO
from app.repo.UserRepo import UserRepo
from app.exceptions import ValidationError

class RegisterService:
    def __init__(self):
        self.user_repo = UserRepo()
    
    def _generate_random_password(self, length=12) -> str:
        """
        Generate a secure random password.

        :param length: Length of the password.
        :return: A securely generated random password string.
        """
        characters = string.ascii_letters + string.digits + string.punctuation
        # Exclude characters that might be problematic in emails
        characters = characters.replace('"', '').replace("'", '').replace('\\', '').replace('/', '')
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    
    def register_user(self, register_dto: RegisterDTO):
        user_dto = self.user_repo.get_user_by_email(register_dto.email)
        if user_dto is not None and self.user_repo.check_user_role(user_dto.user_id, register_dto.role_name):
            raise ValidationError(f"Username '{register_dto.username}' is already taken.")
        
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