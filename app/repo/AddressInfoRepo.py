from app.models.AddressInfoModel import AddressInfoDto
from app.utils.database import get_db_connection
from typing import List
from app.exceptions import handle_exception

class AddressInfoRepo:
    @staticmethod
    def save_address_info(address_info: AddressInfoDto) -> None:
        """
        Insert an address info record into the database.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO AddressInfo (user_id, first_name, last_name, phone, address_line_1, address_line_2, zip_code, latitude, longitude)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (address_info.user_id, address_info.first_name, address_info.last_name, address_info.phone, address_info.address_line_1, address_info.address_line_2, address_info.zip_code, address_info.latitude, address_info.longitude))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            handle_exception(e)

    @staticmethod
    def find_address_info(user_id: str) -> List[AddressInfoDto]:
        """
        Retrieve the address info record from the database by address_id.
        """
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
                SELECT address_id, user_id, first_name, last_name, phone, address_line_1, address_line_2, zip_code, latitude, longitude
                FROM AddressInfo
                WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            return [AddressInfoDto(*row) for row in rows] if rows else []
        
    @staticmethod
    def check_address_exists(user_id: str, address_id: str) -> bool:
        """
        Check if an address exists in the database.
        """
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
                SELECT EXISTS (
                    SELECT 1 
                    FROM AddressInfo 
                    WHERE user_id = %s and address_id = %s
                )
            """
            cursor.execute(query, (user_id, address_id))
            return cursor.fetchone() is not None