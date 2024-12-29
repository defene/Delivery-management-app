from dataclasses import dataclass

@dataclass
class UserDto:
    user_id: int = -1
    username: str = 'invalid'
    password_hash: str = 'invalid'
    email: str = 'invalid'
    enabled: bool = False
    
