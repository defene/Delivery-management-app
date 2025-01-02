from app.models.OrderModel import OrderModel
from app.utils.database import get_db_connection
from app.exceptions import DatabaseError

class OrderRepo:
    @staticmethod
    def create_order(order_model: OrderModel) -> None:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO `Orders` (
                        user_id, 
                        station_id,
                        delivery_src_address_id,
                        delivery_dst_address_id,
                        created_at,
                        updated_at,
                        expected_at,
                        total_price,
                        order_status,
                        delivery_method,
                        category,
                        payload,
                        package_size,
                        notes
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    order_model.user_id, 
                    order_model.station_id, 
                    order_model.delivery_src_address_id,
                    order_model.delivery_dst_address_id,
                    order_model.created_at,
                    order_model.updated_at,
                    order_model.expected_at,
                    order_model.total_price,
                    order_model.order_status,
                    order_model.delivery_method,
                    order_model.category,
                    order_model.payload,
                    order_model.package_size,
                    order_model.notes
                ))
            conn.commit()          
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Error creating order {order_model.order_id}: {e}")
