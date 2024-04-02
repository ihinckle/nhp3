from enum import Enum


class SoSPackage:
    DELIVERY_STATUS = Enum('DeliveryStatus', ['AT_HUB', 'EN_ROUTE', 'DELIVERED'])

    def __init__(self, package):
        self._delivery_status = self.DELIVERY_STATUS.AT_HUB.value
        self._id = package[0]
        self._address = package[1]
        self._city = package[2]
        self._state = package[3]
        self._zip_code = package[4]
        self._deadline = package[5]
        self._weight = package[6]
        self._special_note = package[7]

    def get_id(self) -> str:
        return self._id

    def get_address(self):
        return self._address

    def get_city(self):
        return self._city

    def get_state(self):
        return self._state

    def get_zip(self):
        return self._zip_code

    def get_deadline(self):
        return self._deadline

    def get_weight(self):
        return self._weight

    def get_special_note(self):
        return self._special_note

    def get_delivery_status(self):
        return self._delivery_status

    def set_delivery_status(self, delivery_status):
        self._delivery_status = delivery_status
