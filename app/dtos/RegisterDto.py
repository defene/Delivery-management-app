from dataclasses import dataclass

@dataclass
class RegisterDTO:
    user_id: int = -1
    email: str = 'invalid'
    password: str = 'invalid'
    username: str = 'invalid'
    first_name: str = 'invalid'
    last_name: str = 'invalid'
    role_name: str = 'invalid'