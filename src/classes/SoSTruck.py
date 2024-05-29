import sys
from datetime import datetime
from datetime import timedelta

from src.classes.SoSLocations import SoSLocations
from src.classes.SoSPackage import SoSPackage
from src.classes.SoSPackages import SoSPackages


class SoSTruck:
    @staticmethod
    def _map_delivered_with_to_array(x):
        to_return = [x[0]]
        to_return.extend(x[1].split(', '))
        return to_return

    def __init__(self, number):
        # truck number
        self._truck_number = str(number)
        # max cargo
        self._max_cargo = 16
        # stores package ids
        self._cargo = []
        # average speed
        self._mph = 18
        # passage of time for one mile
        self._minutes_per_mile = 60/self._mph
        # total distance travelled
        self._miles_traveled = 0
        # id of current location
        self._current_location_id = 0
        # stores destination lookup ids for the packages loaded
        self._destinations = []
        # truck clock
        self._clock = datetime.strptime('8:00', '%H:%M')

    def get_truck_number(self):
        return self._truck_number

    def get_miles_traveled(self):
        return self._miles_traveled

    def get_time(self):
        return self._clock

    def is_full(self):
        return len(self._cargo) == self._max_cargo

    def is_empty(self):
        return len(self._cargo) == 0

    def load_truck(self):
        self._load_truck_process()
        while not self.is_full() and len(SoSPackages.delayed) > 0:
            self._wait_for_delayed()
            self._load_truck_process()
        while not self.is_full() and len(SoSPackages.wrong_address) > 0:
            self._wait_for_wrong_address()
            self._load_truck_process()

    def _load_truck_process(self):
        packages_to_load = []
        if len(SoSPackages.truck_restricted) > 0 and len(packages_to_load) < self._max_cargo:
            filtered = filter(lambda x: x[1] == self.get_truck_number(), SoSPackages.truck_restricted)
            filtered_list = list(filtered)
            mapped = map(lambda x: x[0], filtered_list)
            mapped_list = list(mapped)
            packages_to_load.extend(mapped_list)
        if len(SoSPackages.delivered_with) > 0 and len(packages_to_load) < self._max_cargo:
            mapped = map(self._map_delivered_with_to_array, SoSPackages.delivered_with)
            mapped_list = list(mapped)
            for group in mapped_list:
                packages_to_load.extend(group)
        if len(SoSPackages.before_specified_time) > 0 and len(packages_to_load) < self._max_cargo:
            mapped = map(lambda x: x[0], SoSPackages.before_specified_time)
            mapped_list = list(mapped)
            packages_to_load.extend(mapped_list)
        if len(SoSPackages.wrong_address) > 0 and len(packages_to_load) < self._max_cargo:
            filtered = filter(lambda x: datetime.strptime(x[1], '%H:%M %p') >= self._clock, SoSPackages.wrong_address)
            filtered_list = list(filtered)
            for item in filtered_list:
                SoSPackages.packages.get(item[0]).set_address(item[2])
                SoSPackages.packages.get(item[0]).set_zip_code(item[3])
            mapped = map(lambda x: x[0], filtered_list)
            mapped_list = list(mapped)
            packages_to_load.extend(mapped_list)
        if len(packages_to_load) < self._max_cargo:
            for package in SoSPackages.packages:
                if package.get_delivery_status() != SoSPackage.DELIVERY_STATUS.AT_HUB.value:
                    continue
                if package.get_id() in packages_to_load:
                    continue
                packages_to_load.append(package.get_id())
            SoSPackages.packages.reset_iterator()
        while not self.is_full() and len(packages_to_load) > 0:
            package: SoSPackage = SoSPackages.packages.get(packages_to_load.pop(0))
            if package.get_special_note() and package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.DELAYED.value:
                if datetime.strptime(package.get_special_note()[1], '%H:%M %p') > self._clock:
                    continue
                else:
                    SoSPackages.delayed.remove((package.get_id(), package.get_special_note()[1]))
            elif package.get_special_note() and package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.WRONG_ADDRESS.value:
                if self._clock < datetime.strptime('10:20 am', '%H:%M %p'):
                    continue
                else:
                    filtered = filter(lambda x: x[0] == package.get_id(), SoSPackages.wrong_address)
                    filtered_list = list(filtered)
                    SoSPackages.wrong_address.remove(filtered_list[0])
            self._load_package(package)
            self._load_more(SoSLocations.packages_to_locations.get(package.get_destination_lookup_id()))

    def _wait_for_delayed(self):
        self._clock = datetime.strptime(SoSPackages.delayed[0][1], '%H:%M %p')

    def _wait_for_wrong_address(self):
        self._clock = datetime.strptime(SoSPackages.wrong_address[0][1], '%H:%M %p')

    def perform_deliveries(self):
        while not self.is_empty():
            self._go_next_destination()
            self._deliver_packages()
        self._go_next_destination(destination='0')

    def _load_package(self, package: SoSPackage):
        if self.is_full():
            return
        if package.get_delivery_status() != SoSPackage.DELIVERY_STATUS.AT_HUB.value:
            return
        self._cargo.append(package.get_id())
        destination_id = SoSLocations.locations.get(package.get_destination_lookup_id()).get_id()
        if destination_id not in self._destinations:
            self._destinations.append(destination_id)
        SoSPackages.packages_at_hub -= 1
        package.set_delivery_status(SoSPackage.DELIVERY_STATUS.EN_ROUTE.value)
        package.set_loaded_time(self._clock)
        SoSPackages.truck_restricted = list(filter(lambda x: x[0] != package.get_id(), SoSPackages.truck_restricted))
        SoSPackages.before_specified_time = list(filter(lambda x: x[0] != package.get_id(), SoSPackages.before_specified_time))

    def _load_more(self, packages: list):
        if len(packages) < 1:
            return
        while not self.is_full():
            if len(packages) > 0:
                package = SoSPackages.packages.get(packages.pop(0))
                self._load_package(package)
            else:
                break

    def _go_next_destination(self, destination=''):
        if destination:
            distance_to_travel = float(SoSLocations.lookup_distance(self._current_location_id, destination))
            next_destination_id = destination
        else:
            distance_to_travel = sys.maxsize
            for destination_id in self._destinations:
                distance_to_location = float(SoSLocations.lookup_distance(self._current_location_id, destination_id))
                if distance_to_location < distance_to_travel:
                    distance_to_travel = distance_to_location
                    next_destination_id = destination_id
        self._miles_traveled += distance_to_travel
        self._clock += timedelta(minutes=self._minutes_per_mile*distance_to_travel)
        self._current_location_id = next_destination_id

    def _deliver_packages(self):
        packages_to_remove = []
        for package_id in self._cargo:
            package: SoSPackage = SoSPackages.packages.get(package_id)
            if SoSLocations.locations.get(package.get_destination_lookup_id()).get_id() == self._current_location_id:
                packages_to_remove.append(package_id)
                package.set_delivery_status(SoSPackage.DELIVERY_STATUS.DELIVERED.value)
                package.set_delivered_time(self._clock)
        for package_id in packages_to_remove:
            self._cargo.remove(package_id)
        self._destinations.remove(self._current_location_id)


    def print_cargo(self):
        print(self._truck_number, ':', self._cargo)

    def print_destinations(self):
        print(self._truck_number, ':', self._destinations)
