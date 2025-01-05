from app.models.OrderModel import OrderModel
from app.utils.database import get_db_connection
from app.exceptions import DatabaseError
from typing import List

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
        
    @staticmethod
    def delete_order(order_id: int) -> None:
        """
        Deletes an order from the database based on the given order_id.
        
        :param order_id: The ID of the order to be deleted.
        :raises DatabaseError: If an error occurs during the database operation.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = "DELETE FROM `Orders` WHERE order_id = %s"
                cursor.execute(query, (order_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Error deleting order with ID {order_id}: {e}")
        
    @staticmethod
    def get_orders_by_user(user_id: int) -> List[OrderModel]:
        """
        Retrieves all orders for a specific user ID.

        :param user_id: The ID of the user whose orders are to be retrieved.
        :return: A list of OrderModel instances representing the user's orders.
        :raises DatabaseError: If an error occurs during the database operation.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        order_id, 
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
                    FROM `Orders`
                    WHERE user_id = %s
                """
                cursor.execute(query, (user_id,))
                results = cursor.fetchall()
                # Convert results to a list of OrderModel instances
                orders = [
                    OrderModel(
                        order_id=row[0],
                        user_id=row[1],
                        station_id=row[2],
                        delivery_src_address_id=row[3],
                        delivery_dst_address_id=row[4],
                        created_at=row[5],
                        updated_at=row[6],
                        expected_at=row[7],
                        total_price=row[8],
                        order_status=row[9],
                        delivery_method=row[10],
                        category=row[11],
                        payload=row[12],
                        package_size=row[13],
                        notes=row[14]
                    )
                    for row in results
                ]
                return orders
        except Exception as e:
            raise DatabaseError(f"Error fetching orders for user ID {user_id}: {e}")