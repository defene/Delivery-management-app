from dataclasses import dataclass

@dataclass
class UserDto:
    user_id: int
    username: str
    password_hash: str
    email: str
    enabled: bool
