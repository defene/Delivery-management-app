from dataclasses import dataclass

@dataclass
class StationDto:
    station_id: int = -1
    station_name: str = ''
    address_line_1: str = ''
    address_line_2: str = ''
    zip_code: str = ''
    latitude: float = 0.0
    longitude: float = 0.0
    max_drone_capacity: int = 0
    max_robot_capacity: int = 0
    current_drone_count: int = 0
    current_robot_count: int = 0
    current_available_drone_count: int = 0
    current_available_robot_count: int = 0
    current_working_drone_count: int = 0
    current_working_robot_count: int = 0
    dispatch_strategy: str = ''
    enabled: bool = False
