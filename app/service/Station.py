from app.models.StationModel import StationDto
from app.repo.StationRepo import StationRepo

class StationService:
    def __init__(self):
        pass

    def save_station(self, station_data: dict):
        """
        Receive a dictionary containing station information, map it to a StationDto,
        then call the repo layer to save it to the database.
        """
        station_dto = StationDto(
            # If station_data has station_id but this is a new entry, you can default to -1 or ignore it.
            station_id=station_data.get('station_id', -1),
            station_name=station_data.get('station_name', ''),
            address_line_1=station_data.get('address_line_1', ''),
            address_line_2=station_data.get('address_line_2', ''),
            zip_code=station_data.get('zip_code', ''),
            latitude=station_data.get('latitude', 0.0),
            longitude=station_data.get('longitude', 0.0),
            max_drone_capacity=station_data.get('max_drone_capacity', 0),
            max_robot_capacity=station_data.get('max_robot_capacity', 0),
            current_drone_count=station_data.get('current_drone_count', 0),
            current_robot_count=station_data.get('current_robot_count', 0),
            current_available_drone_count=station_data.get('current_available_drone_count', 0),
            current_available_robot_count=station_data.get('current_available_robot_count', 0),
            current_working_drone_count=station_data.get('current_working_drone_count', 0),
            current_working_robot_count=station_data.get('current_working_robot_count', 0),
            dispatch_strategy=station_data.get('dispatch_strategy', ''),
            enabled=station_data.get('enabled', False)
        )

        return StationRepo.save_station(station_dto)

    def find_station_by_id(self, station_id: int) -> StationDto:
        """
        Retrieve station information by station_id.
        """
        return StationRepo.find_station_by_id(station_id)

    def find_all_stations(self):
        """
        Retrieve all station records from the database.
        """
        return StationRepo.find_all_stations()

    def update_station(self, station_data: dict):
        """
        Update station information. station_id must be provided in station_data.
        """
        if 'station_id' not in station_data:
            raise ValueError("station_id is required for updating a station.")

        station_dto = StationDto(
            station_id=station_data['station_id'],
            station_name=station_data.get('station_name', ''),
            address_line_1=station_data.get('address_line_1', ''),
            address_line_2=station_data.get('address_line_2', ''),
            zip_code=station_data.get('zip_code', ''),
            latitude=station_data.get('latitude', 0.0),
            longitude=station_data.get('longitude', 0.0),
            max_drone_capacity=station_data.get('max_drone_capacity', 0),
            max_robot_capacity=station_data.get('max_robot_capacity', 0),
            current_drone_count=station_data.get('current_drone_count', 0),
            current_robot_count=station_data.get('current_robot_count', 0),
            current_available_drone_count=station_data.get('current_available_drone_count', 0),
            current_available_robot_count=station_data.get('current_available_robot_count', 0),
            current_working_drone_count=station_data.get('current_working_drone_count', 0),
            current_working_robot_count=station_data.get('current_working_robot_count', 0),
            dispatch_strategy=station_data.get('dispatch_strategy', ''),
            enabled=station_data.get('enabled', False)
        )

        return StationRepo.update_station(station_dto)

    def delete_station(self, station_id: int):
        """
        Delete a station record by station_id.
        """
        return StationRepo.delete_station(station_id)

    def find_all_stations_availability(self):
        """
        Retrieve the available drone/robot counts for all stations.
        Returns a list of dictionaries, each containing:
            {
                'station_id': ...,
                'station_name': ...,
                'available_drones': ...,
                'available_robots': ...
            }
        """
        stations: list[StationDto] = StationRepo.find_all_stations()
        result = []
        for s in stations:
            item = {
                'station_id': s.station_id,
                'station_name': s.station_name,
                'station_address': f"{s.address_line_1} {s.address_line_2 if s.address_line_2 else ''}",
                'available_drones': s.current_available_drone_count,
                'available_robots': s.current_available_robot_count
            }
            result.append(item)

        return result
