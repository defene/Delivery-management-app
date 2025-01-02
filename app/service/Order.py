from app.dtos.OrderDto import OrderDTO
from app.repo.OrderRepo import OrderRepo
from app.repo.AddressInfoRepo import AddressInfoRepo
from app.repo.StationRepo import StationRepo
from app.exceptions import AuthenticationError

from datetime import datetime, timedelta

class OrderService:
    def __init__(self):
        self.order_repo = OrderRepo()
        self.address_repo = AddressInfoRepo()
        self.station_repo = StationRepo()
        
    def create_order(self, order_dto: OrderDTO):
        if not self.station_repo.check_station_exists(order_dto.station_id):
            raise AuthenticationError("Station does not exist.")
        if not self.address_repo.check_address_exists(order_dto.source_address_id):
            raise AuthenticationError("Source address does not exist.")
        if not self.address_repo.check_address_exists(order_dto.dest_address_id):
            raise AuthenticationError("Destination address does not exist.")