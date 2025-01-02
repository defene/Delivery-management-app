from typing import Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class OrderModel:
    order_id: int = -1
    user_id: int = -1
    station_id: int = -1
    delivery_src_address_id: int = -1
    delivery_dst_address_id: int = -1
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    expected_at: Optional[datetime] = None
    total_price: float = 0.0
    order_status: Optional[str] = None
    delivery_method: Optional[str] = None
    category: Optional[str] = None
    payload: float = 0.0
    package_size: Optional[str] = None
    notes: Optional[str] = None