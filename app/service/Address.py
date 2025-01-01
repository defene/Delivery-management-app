from app.models.AddressInfoModel import AddressInfoDto
from app.repo.AddressInfoRepo import AddressInfoRepo


class AddressService:
    def __init__(self):
        pass

    def save_address_info(self, user_id, address_info):
        address_info = AddressInfoDto(
            user_id=user_id,
            first_name=address_info['first_name'],
            last_name=address_info['last_name'],
            phone=address_info['phone'],
            address_line_1=address_info['address_line_1'],
            address_line_2=address_info['address_line_2'],
            zip_code=address_info['zip_code'],
            latitude=address_info.get('latitude', 0),
            longitude=address_info.get('longitude', 0)
        )
        
        return AddressInfoRepo.save_address_info(address_info)
    
    def find_address_info(self, user_id):
        return AddressInfoRepo.find_address_info(user_id)
