from dataclasses import dataclass

@dataclass
class LoginDto:
    email: str = 'invalid'
    password: str = 'invalid'
    role_name: str = 'invalid'