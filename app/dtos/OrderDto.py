from typing import Optional
from dataclasses import dataclass

@dataclass
class OrderDTO:
    station_id: int = -1
    user_id: int = -1
    source_address_id: int = -1
    dest_address_id: int = -1
    delivery_method: str = 'robot'
    total_price: float = -1.0
    package_size_length: float = -1.0
    package_size_width: float = -1.0
    package_size_height: float = -1.0
    package_weight: float = -1.0
    category: Optional[str] = None
    distance: float = -1.0
    duration: float = -1.0
    notes: Optional[str] = None
    