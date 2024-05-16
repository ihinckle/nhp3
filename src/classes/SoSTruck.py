from datetime import datetime

from src.classes.SoSPackage import SoSPackage
from src.classes.SoSPackages import SoSPackages


class SoSTruck:
    def __init__(self, number):
        self._is_full = False
        self._cargo = []
        self._destinations = []
        self._truck_number = str(number)
        self._clock = datetime.strptime('08:00', '%H:%M:%S')

    def get_truck_number(self):
        return self._truck_number

    def is_full(self):
        return self._is_full

    def load(self, package: SoSPackage):
        if len(self._cargo) == 16:
            self._is_full = True
            return
        if package.get_delivery_status() != SoSPackage.DELIVERY_STATUS.AT_HUB.value:
            return
        self._cargo.append(package.get_id())
        if package.get_destination_id() not in self._destinations:
            self._destinations.append(package.get_destination_id())
        package.set_delivery_status(SoSPackage.DELIVERY_STATUS.EN_ROUTE.value)
        SoSPackages.truck_restricted = list(filter(lambda x: x[0] != package.get_id(), SoSPackages.truck_restricted))
        SoSPackages.before_specified_time = list(filter(lambda x: x[0] != package.get_id(), SoSPackages.before_specified_time))

    def print_cargo(self):
        print(self._truck_number, ':', self._cargo)

    def print_destinations(self):
        print(self._truck_number, ':', self._destinations)
