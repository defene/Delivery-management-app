import datetime
from dataclasses import dataclass

@dataclass
class OrderModel:
    order_id = -1
    user_id = -1
    station_id = -1
    delivery_src_address_id = -1
    delivery_dst_address_id = -1
    created_at = -1
    expected_at = -1
    total_price = -1.0
    delivery_method = 'robot'
    category = None
    payload = -1.0
    package_size = None
    notes = None