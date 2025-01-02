from dataclasses import dataclass

@dataclass
class OrderDTO:
    station_id = -1
    user_id = -1
    source_address_id = -1
    dest_address_id = -1
    delivery_method = 'robot'
    total_price = -1.0
    package_size_length = -1.0
    package_size_width = -1.0
    package_size_height = -1.0
    package_weight = -1.0
    category = None
    distance = -1.0
    duration = -1.0
    notes = None
    