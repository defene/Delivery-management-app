from app.utils.database import get_db_connection
from app.exceptions import DatabaseError
from app.models.StationModel import StationDto

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
        
    
    @staticmethod
    def find_all_stations() -> list:
        """
        Retrieve all station records from the database.
        """
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        station_id,
                        station_name,
                        address_line_1,
                        address_line_2,
                        zip_code,
                        latitude,
                        longitude,
                        max_drone_capacity,
                        max_robot_capacity,
                        current_drone_count,
                        current_robot_count,
                        current_available_drone_count,
                        current_available_robot_count,
                        current_working_drone_count,
                        current_working_robot_count,
                        dispatch_strategy,
                        enabled
                    FROM Station
                    WHERE enabled = 1
                """
                cursor.execute(query)
                stations = cursor.fetchall()

                return [StationDto(*row) for row in stations] if stations else []
        except Exception as e:
            raise DatabaseError(f"Error fetching stations: {e}")