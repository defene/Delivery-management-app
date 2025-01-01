from dataclasses import dataclass

@dataclass
class AddressInfoDto:
    address_id: int = -1
    user_id: int = -1
    first_name: str = 'invalid'
    last_name: str = 'invalid'
    phone: str = 'invalid'
    address_line_1: str = 'invalid'
    address_line_2: str = 'invalid'
    zip_code: str = 'invalid'
    latitude: float = 0.0
    longitude: float = 0.0
