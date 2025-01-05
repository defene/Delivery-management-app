from dataclasses import dataclass

@dataclass
class UserDto:
    # 传入元组时候的初始化
    def __init__(self, user_tuple):
        self.user_id = user_tuple[0]
        self.username = user_tuple[1]
        self.password_hash = user_tuple[2]
        self.email = user_tuple[3]
        self.enabled = user_tuple[4]

    user_id: int = -1
    username: str = 'invalid'
    password_hash: str = 'invalid'
    email: str = 'invalid'
    enabled: bool = False


class UserWithoutPasswordDto:
    # 传入元组时候的初始化
    def __init__(self, user_tuple):
        self.user_id = user_tuple[0]
        self.username = user_tuple[1]
        self.user_first_name = user_tuple[2]
        self.user_last_name = user_tuple[3]
        self.email = user_tuple[5]
        self.enabled = user_tuple[6]

    user_id: int = -1
    username: str = 'invalid'
    user_first_name: str = 'invalid'
    user_last_name: str = 'invalid'
    email: str = 'invalid'
    enabled: bool = False
