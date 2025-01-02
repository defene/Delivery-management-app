import re

from app.dtos.OrderDto import OrderDTO
from app.models.OrderModel import OrderModel
from app.repo.OrderRepo import OrderRepo
from app.repo.AddressInfoRepo import AddressInfoRepo
from app.repo.StationRepo import StationRepo
from app.repo.UserRepo import UserRepo
from app.exceptions import AuthenticationError

from datetime import datetime, timedelta

class OrderService:
    def __init__(self):
        self.order_repo = OrderRepo()
        self.address_repo = AddressInfoRepo()
        self.station_repo = StationRepo()
        self.user_repo = UserRepo()
        
    def _parse_duration(self, duration_str):
        """
        Parses a duration string like "15 mins" or "2 hours" and returns a corresponding timedelta object.

        :param duration_str: A string representing the duration, e.g., "15 mins", "2 hours"
        :return: timedelta object representing the parsed duration
        """
        pattern = r'(?P<value>\d+)\s*(?P<unit>hours?|hrs?|minutes?|mins?)'
        match = re.match(pattern, duration_str.lower())
        if not match:
            raise ValueError(f"Invalid duration format: {duration_str}")
        
        value = int(match.group('value'))
        unit = match.group('unit')
        
        if unit.startswith('hour') or unit.startswith('hr'):
            return timedelta(hours=value)
        elif unit.startswith('min'):
            return timedelta(minutes=value)
        else:
            raise ValueError(f"Unknown duration unit: {unit}")
        
    def create_order(self, order_dto: OrderDTO):
        if not self.station_repo.check_station_exists(order_dto.station_id):
            raise AuthenticationError("Station does not exist.")
        if not self.user_repo.check_user_exists(order_dto.user_id):
            raise AuthenticationError("User does not exist.")
        if not self.address_repo.check_address_exists(order_dto.user_id, order_dto.source_address_id):
            raise AuthenticationError("Source address does not exist.")
        if not self.address_repo.check_address_exists(order_dto.user_id, order_dto.dest_address_id):
            raise AuthenticationError("Destination address does not exist.")
        
        duration = self._parse_duration(order_dto.duration)
        
        order_model = OrderModel(
            station_id=order_dto.station_id,
            user_id=order_dto.user_id,
            delivery_src_address_id=order_dto.source_address_id,
            delivery_dst_address_id=order_dto.dest_address_id,
            delivery_method=order_dto.delivery_method,
            total_price=order_dto.total_price,
            order_status='pending',
            package_size=f"{order_dto.package_size_length}x{order_dto.package_size_width}x{order_dto.package_size_height}",
            payload=order_dto.package_weight,
            category=order_dto.category,
            notes=order_dto.notes,
            created_at=datetime.now(),
            expected_at=datetime.now() + duration,
            updated_at=datetime.now()
        )
        
        order_id = self.order_repo.create_order(order_model)
        return order_id