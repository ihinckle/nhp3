from enum import Enum
import re


class SoSPackage:
    DELIVERY_STATUS = Enum('DeliveryStatus', ['AT_HUB', 'EN_ROUTE', 'DELIVERED'])
    SPECIAL_NOTE_TYPE = Enum('SpecialNoteType', ['TRUCK_LIMITATION', 'DELAYED', 'WRONG_ADDRESS', 'DELIVERED_WITH'])
    NO_DEADLINE = 'EOD'

    def __init__(self, package):
        self._delivery_status: int = self.DELIVERY_STATUS.AT_HUB.value
        self._id: str = package[0]
        self._address: str = package[1]
        self._city: str = package[2]
        self._state: str = package[3]
        self._zip_code: str = package[4]
        self._deadline: str = package[5]
        self._weight: str = package[6]
        self._special_note: tuple = self._parse_special_note(package)
        self._loaded_time = -1
        self._delivered_time = -1

    def get_id(self) -> str:
        return self._id

    def get_address(self) -> str:
        return self._address

    def get_city(self) -> str:
        return self._city

    def get_state(self) -> str:
        return self._state

    def get_zip(self) -> str:
        return self._zip_code

    def get_deadline(self) -> str:
        return self._deadline

    def get_weight(self):
        return self._weight

    def get_special_note(self):
        return self._special_note

    def get_delivery_status(self):
        return self._delivery_status

    def set_delivery_status(self, delivery_status):
        self._delivery_status = delivery_status

    def get_destination_id(self) -> str:
        return self.get_address()+self.get_zip()

    def get_loaded_time(self):
        return self._loaded_time

    def set_loaded_time(self, time):
        self._loaded_time = time

    def get_delivered_time(self):
        return self._delivered_time

    def set_delivered_time(self, time):
        self._delivered_time = time

    def _parse_special_note(self, package):
        special_note = package[7]
        if matched := re.compile('\D*truck.*(\d)').match(special_note):
            special_note = (self.SPECIAL_NOTE_TYPE.TRUCK_LIMITATION.value, matched.group(1))
        elif matched := re.compile('Delayed.*?(\d+:\d+ [ap]m)').match(special_note):
            special_note = (self.SPECIAL_NOTE_TYPE.DELAYED.value, matched.group(1))
        elif re.compile('Wrong.*').match(special_note):
            special_note = (self.SPECIAL_NOTE_TYPE.WRONG_ADDRESS.value,)
        elif matched := re.compile('(Must\D*)(?(1)((?:\d+, )*\d*))').match(special_note):
            special_note = (self.SPECIAL_NOTE_TYPE.DELIVERED_WITH.value, matched.group(2))
        return special_note
