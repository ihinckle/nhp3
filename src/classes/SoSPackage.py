from enum import Enum


class SoSPackage:
    DELIVERY_STATUS = Enum('DeliveryStatus', ['AT_HUB', 'EN_ROUTE', 'DELIVERED'])

    def __init__(self, package):
        self.__delivery_status = self.DELIVERY_STATUS.AT_HUB.value
        self.__id = package[0]
        self.__address = package[1]
        self.__city = package[2]
        self.__state = package[3]
        self.__zip_code = package[4]
        self.__deadline = package[5]
        self.__weight = package[6]
        self.__special_note = package[7]

    def get_id(self) -> str:
        return self.__id

    def get_address(self):
        return self.__address

    def get_city(self):
        return self.__city

    def get_state(self):
        return self.__state

    def get_zip(self):
        return self.__zip_code

    def get_deadline(self):
        return self.__deadline

    def get_weight(self):
        return self.__weight

    def get_special_note(self):
        return self.__special_note

    def get_delivery_status(self):
        return self.__delivery_status

    def set_delivery_status(self, delivery_status):
        self.__delivery_status = delivery_status
