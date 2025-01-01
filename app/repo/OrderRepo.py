from typing import Optional
from app.dtos.OrderDto import OrderDto
from app.utils.database import get_db_connection

class OrderRepo:
    @staticmethod
    def create_order(order_dto: OrderDto) -> None:
        pass
