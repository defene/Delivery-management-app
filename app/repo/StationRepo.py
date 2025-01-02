from app.utils.database import get_db_connection
from app.exceptions import DatabaseError

class StationRepo:
    @staticmethod
    def check_station_exists(station_id: str) -> bool:
        """
        Check if the station exists in the database.
        """
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                query = """
                    SELECT EXISTS (
                        SELECT 1 
                        FROM Station 
                        WHERE station_id = %s
                    )
                """
                cursor.execute(query, (station_id,))
                count = cursor.fetchone()[0]
                return count > 0
        except Exception as e:
            raise DatabaseError(f"Error checking station {station_id}: {e}")