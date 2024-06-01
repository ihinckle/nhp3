import sys
from datetime import datetime
from datetime import timedelta

from src.classes.SoSLocations import SoSLocations
from src.classes.SoSPackage import SoSPackage
from src.classes.SoSPackages import SoSPackages


class SoSTruck:
    # Maps the tuple of packages that have required outgoing packages with them into an array for later.
    @staticmethod
    def _map_delivered_with_to_array(x):
        to_return = [x[0]]
        to_return.extend(x[1].split(', '))
        return to_return

    # Initialize class.
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

    # Load truck is called by the program to get everything started and onto the truck.
    def load_truck(self):
        # We start by loading the truck.
        self._load_truck_process()
        # Then we check if the truck is full.
        # If the truck is not full and there are delayed packages then we wait for those to arrive.
        while not self.is_full() and len(SoSPackages.delayed) > 0:
            self._wait_for_delayed()
            self._load_truck_process()
        # if the truck is not full and the corrected package has not been loaded then we wait for the correction.
        while not self.is_full() and len(SoSPackages.wrong_address) > 0:
            self._wait_for_wrong_address()
            self._load_truck_process()

    # This actually loads the truck.
    def _load_truck_process(self):
        # We will build an array that we can simply grab from and toss the packages on.
        packages_to_load = []
        # We start by preparing any truck restricted packages.
        if len(SoSPackages.truck_restricted) > 0 and len(packages_to_load) < self._max_cargo:
            filtered = filter(lambda x: x[1] == self.get_truck_number(), SoSPackages.truck_restricted)
            filtered_list = list(filtered)
            mapped = map(lambda x: x[0], filtered_list)
            mapped_list = list(mapped)
            packages_to_load.extend(mapped_list)
        # Then we prepare any packages that have required packages that go out with them.
        if len(SoSPackages.delivered_with) > 0 and len(packages_to_load) < self._max_cargo:
            mapped = map(self._map_delivered_with_to_array, SoSPackages.delivered_with)
            mapped_list = list(mapped)
            for group in mapped_list:
                packages_to_load.extend(group)
        # Then we check and see if the delayed packages can be prepared.
        if len(SoSPackages.before_specified_time) > 0 and len(packages_to_load) < self._max_cargo:
            mapped = map(lambda x: x[0], SoSPackages.before_specified_time)
            mapped_list = list(mapped)
            packages_to_load.extend(mapped_list)
        # Then we check if the corrected address package can be prepared.
        if len(SoSPackages.wrong_address) > 0 and len(packages_to_load) < self._max_cargo:
            filtered = filter(lambda x: datetime.strptime(x[1], '%H:%M %p') >= self._clock, SoSPackages.wrong_address)
            filtered_list = list(filtered)
            for item in filtered_list:
                SoSPackages.packages.get(item[0]).set_address(item[2])
                SoSPackages.packages.get(item[0]).set_zip_code(item[3])
            mapped = map(lambda x: x[0], filtered_list)
            mapped_list = list(mapped)
            packages_to_load.extend(mapped_list)
        # Lastly we prepare any packages left at the hub that don't have any special conditions.
        if len(packages_to_load) < self._max_cargo:
            for package in SoSPackages.packages:
                if package.get_delivery_status() != SoSPackage.DELIVERY_STATUS.AT_HUB.value:
                    continue
                if package.get_id() in packages_to_load:
                    continue
                packages_to_load.append(package.get_id())
            SoSPackages.packages.reset_iterator()
        # Now we start loading packages from the prepared array.
        while not self.is_full() and len(packages_to_load) > 0:
            # Grab the package at the front.
            package: SoSPackage = SoSPackages.packages.get(packages_to_load.pop(0))
            if package.get_special_note() and package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.DELAYED.value:
                # Check if it can actually be loaded.
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
            # Load the package.
            self._load_package(package)
            # Greedily grab any other packages from that address and load them.
            self._load_more(SoSLocations.packages_to_locations.get(package.get_destination_lookup_id()))

    # Tell the truck to wait at the hub for delayed packages until it is full.
    def _wait_for_delayed(self):
        self._clock = datetime.strptime(SoSPackages.delayed[0][1], '%H:%M %p')

    # Tell the truck to wait at the hub for the wrong address package.
    def _wait_for_wrong_address(self):
        self._clock = datetime.strptime(SoSPackages.wrong_address[0][1], '%H:%M %p')

    # Called by the program to send the truck out to perform the deliveries.
    def perform_deliveries(self):
        # Loop until the truck is empty.
        while not self.is_empty():
            self._go_next_destination()
            self._deliver_packages()
        # Go back to the hub.
        self._go_next_destination(destination='0')

    # Load a package onto the truck.
    def _load_package(self, package: SoSPackage):
        # Check if there is room.
        if self.is_full():
            return
        # Double check that the package is actually at the hub.
        if package.get_delivery_status() != SoSPackage.DELIVERY_STATUS.AT_HUB.value:
            return
        # Add the package to the cargo manifest.
        self._cargo.append(package.get_id())
        # Add the destination id to the gps destinations. Each entry in the array will be unique.
        destination_id = SoSLocations.locations.get(package.get_destination_lookup_id()).get_id()
        if destination_id not in self._destinations:
            self._destinations.append(destination_id)
        # Count down the packages at the hub.
        SoSPackages.packages_at_hub -= 1
        # Set the package to en route.
        package.set_delivery_status(SoSPackage.DELIVERY_STATUS.EN_ROUTE.value)
        # Record the loaded time.
        package.set_loaded_time(self._clock)
        # Record which truck delivered the package.
        package.set_on_truck(self._truck_number)
        # Remove the package from its special pile
        SoSPackages.truck_restricted = list(filter(lambda x: x[0] != package.get_id(), SoSPackages.truck_restricted))
        SoSPackages.before_specified_time = list(filter(lambda x: x[0] != package.get_id(), SoSPackages.before_specified_time))

    # Greedily load more packages for the same address.
    def _load_more(self, packages: list):
        if len(packages) < 1:
            return
        while not self.is_full():
            if len(packages) > 0:
                package = SoSPackages.packages.get(packages.pop(0))
                self._load_package(package)
            else:
                break

    # Go to the next destination. We use the nearest neighbor to attempt to minimize the distance travelled.
    def _go_next_destination(self, destination=''):
        # If a destination is defined by the program then go there.
        if destination:
            distance_to_travel = float(SoSLocations.lookup_distance(self._current_location_id, destination))
            next_destination_id = destination
        else:
            # We set the default to the system's max number.
            # This is safe because we do not call this method without
            # a destination id if there are no destination left.
            distance_to_travel = sys.maxsize
            # Loop through the gps destinations.
            for destination_id in self._destinations:
                # Get the destination distance.
                distance_to_location = float(SoSLocations.lookup_distance(self._current_location_id, destination_id))
                # If the distance is less than the current distance.
                if distance_to_location < distance_to_travel:
                    # Replace the distance.
                    distance_to_travel = distance_to_location
                    # Replace the destination id.
                    next_destination_id = destination_id
        # Calculate and add the miles travelled.
        self._miles_traveled += distance_to_travel
        # Calculate and add the time travelled to the truck clock.
        self._clock += timedelta(minutes=self._minutes_per_mile*distance_to_travel)
        # Tell the gps where we are.
        self._current_location_id = next_destination_id

    # Deliver the packages.
    def _deliver_packages(self):
        packages_to_remove = []
        # Loop through the packages in the cargo for anything that should be delivered at the destination.
        for package_id in self._cargo:
            package: SoSPackage = SoSPackages.packages.get(package_id)
            if SoSLocations.locations.get(package.get_destination_lookup_id()).get_id() == self._current_location_id:
                # Add the package to be removed from the manifest.
                # Modifying an array while in the loop is a terrible move.
                packages_to_remove.append(package_id)
                # Set the package as delivered.
                package.set_delivery_status(SoSPackage.DELIVERY_STATUS.DELIVERED.value)
                # Set the delivered time.
                package.set_delivered_time(self._clock)
        # Loop through the packages that were delivered and remove them from the cargo manifest.
        for package_id in packages_to_remove:
            self._cargo.remove(package_id)
        # Remove the destination from the gps.
        self._destinations.remove(self._current_location_id)
