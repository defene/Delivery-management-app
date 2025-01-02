# app/repo/StationRepo.py

from typing import List, Optional
from app.models.StationModel import StationDto
from app.utils.database import get_db_connection
from app.exceptions import handle_exception

class StationRepo:
    @staticmethod
    def save_station(station: StationDto) -> int:
        """
        Insert a station record into the database.
        Returns the number of affected rows (should be 1 if successful).
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO Station (
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
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    station.station_name,
                    station.address_line_1,
                    station.address_line_2,
                    station.zip_code,
                    station.latitude,
                    station.longitude,
                    station.max_drone_capacity,
                    station.max_robot_capacity,
                    station.current_drone_count,
                    station.current_robot_count,
                    station.current_available_drone_count,
                    station.current_available_robot_count,
                    station.current_working_drone_count,
                    station.current_working_robot_count,
                    station.dispatch_strategy,
                    station.enabled
                ))
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            conn.rollback()
            handle_exception(e)
        finally:
            conn.close()

    @staticmethod
    def find_station_by_id(station_id: int) -> Optional[StationDto]:
        """
        Retrieve a station record from the database by station_id.
        Return a StationDto or None if not found.
        """
        conn = get_db_connection()
        try:
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
                    WHERE station_id = %s
                """
                cursor.execute(query, (station_id,))
                row = cursor.fetchone()
                if row:
                    return StationDto(*row)  # 直接用解包传入
                else:
                    return None
        except Exception as e:
            handle_exception(e)
        finally:
            conn.close()

    @staticmethod
    def find_all_stations() -> List[StationDto]:
        """
        Retrieve all station records from the database.
        Return a list of StationDto.
        """
        conn = get_db_connection()
        try:
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
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                return [StationDto(*row) for row in rows] if rows else []
        except Exception as e:
            handle_exception(e)
            return []
        finally:
            conn.close()

    @staticmethod
    def update_station(station: StationDto) -> int:
        """
        Update an existing station record based on station_id.
        Returns the number of affected rows.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    UPDATE Station
                    SET
                        station_name = %s,
                        address_line_1 = %s,
                        address_line_2 = %s,
                        zip_code = %s,
                        latitude = %s,
                        longitude = %s,
                        max_drone_capacity = %s,
                        max_robot_capacity = %s,
                        current_drone_count = %s,
                        current_robot_count = %s,
                        current_available_drone_count = %s,
                        current_available_robot_count = %s,
                        current_working_drone_count = %s,
                        current_working_robot_count = %s,
                        dispatch_strategy = %s,
                        enabled = %s
                    WHERE station_id = %s
                """
                cursor.execute(query, (
                    station.station_name,
                    station.address_line_1,
                    station.address_line_2,
                    station.zip_code,
                    station.latitude,
                    station.longitude,
                    station.max_drone_capacity,
                    station.max_robot_capacity,
                    station.current_drone_count,
                    station.current_robot_count,
                    station.current_available_drone_count,
                    station.current_available_robot_count,
                    station.current_working_drone_count,
                    station.current_working_robot_count,
                    station.dispatch_strategy,
                    station.enabled,
                    station.station_id
                ))
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            conn.rollback()
            handle_exception(e)
            return 0
        finally:
            conn.close()

    @staticmethod
    def delete_station(station_id: int) -> int:
        """
        Delete a station record by station_id.
        Returns the number of affected rows (should be 1 if successful).
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = "DELETE FROM Station WHERE station_id = %s"
                cursor.execute(query, (station_id,))
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            conn.rollback()
            handle_exception(e)
            return 0
        finally:
            conn.close()
