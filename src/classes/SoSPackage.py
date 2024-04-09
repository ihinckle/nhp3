from enum import Enum
import re


class SoSPackage:
    DELIVERY_STATUS = Enum('DeliveryStatus', ['AT_HUB', 'EN_ROUTE', 'DELIVERED'])
    SPECIAL_NOTE_TYPE = Enum('SpecialNoteType', ['TRUCK_LIMITATION'])

    def __init__(self, package):
        self._delivery_status = self.DELIVERY_STATUS.AT_HUB.value
        self._id = package[0]
        self._address = package[1]
        self._city = package[2]
        self._state = package[3]
        self._zip_code = package[4]
        self._deadline = package[5]
        self._weight = package[6]
        self._special_note = self._parse_special_note(package)

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

    def _parse_special_note(self, package):
        special_note = package[7]
        if matched := re.compile('\D*truck.*(\d)').match(special_note):
            special_note = (self.SPECIAL_NOTE_TYPE.TRUCK_LIMITATION.value, matched.group(1))
        return special_note
