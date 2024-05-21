import sys
from datetime import datetime

from src.classes.SoSLocations import SoSLocations
from src.classes.SoSPackage import SoSPackage
from src.classes.SoSPackages import SoSPackages


class SoSTruck:
    def __init__(self, number):
        self._truck_number = str(number)
        self._max_cargo = 16
        self._is_full = False
        self._cargo = []
        self._mph = 18
        self._minutes_per_mile = 60/self._mph
        self._miles_traveled = 0
        self._current_location_id = 0
        self._destinations = []
        self._clock = datetime.strptime('8:00:00', '%H:%M:%S')

    def get_truck_number(self):
        return self._truck_number

    def get_miles_traveled(self):
        return self._miles_traveled

    def is_full(self):
        return self._is_full

    def load(self, package: SoSPackage):
        if len(self._cargo) == self._max_cargo:
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

    def deliver_packages(self):
        while len(self._cargo) > 0:
            self._go_next_destination()

    def _go_next_destination(self):
        if len(self._destinations) > 0:
            distance_to_travel = sys.maxsize
            destination_ids = []
            for destination in self._cargo:
                destination_ids.append(SoSLocations.locations.get(destination).get_id())
            for destination_id in destination_ids:
                distance_to_location = SoSLocations.lookup_distance(self._current_location_id, destination_id)
                if distance_to_location < distance_to_travel:
                    distance_to_travel = distance_to_location
                    next_destination_id = destination_id
        else:
            next_destination_id = 0
        self._miles_traveled += distance_to_travel
        self._current_location_id = next_destination_id

    def print_cargo(self):
        print(self._truck_number, ':', self._cargo)

    def print_destinations(self):
        print(self._truck_number, ':', self._destinations)
