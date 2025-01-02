from flask import Blueprint, jsonify, request
from app.service.Station import StationService

station_controller = Blueprint('station_controller', __name__)
station_service = StationService()

@station_controller.route('/stations', methods=['POST'])
def create_station():
    station_data = request.json
    result = station_service.save_station(station_data)
    return jsonify({"rowcount": result}), 201

@station_controller.route('/stations/availability', methods=['GET'])
def get_stations_availability():
    """
    GET /stations/availability
    Returns the number of available drones/robots for all warehouses
    """
    availability_list = station_service.find_all_stations_availability()
    return jsonify(availability_list), 200
