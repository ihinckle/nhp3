import csv

from src.classes.SoSHashTable import SoSHashTable
from src.classes.SoSLocations import SoSLocations
from src.classes.SoSPackage import SoSPackage


class SoSPackages:
    packages: SoSHashTable
    truck_restricted: list[tuple] = []
    before_specified_time: list[tuple] = []
    delivered_with: list[tuple] = []
    delayed: list[tuple] = []
    wrong_address: list[tuple] = []
    packages_at_hub: int

    # Initialize class.
    @staticmethod
    def initialize():
        with open('resources/packages.csv') as packages_csv:
            # Count how many rows to create a perfectly sized HashTable.
            package_quantity = len(packages_csv.readlines()) - 1
            SoSPackages.packages = SoSHashTable(package_quantity)
            SoSPackages.packages_at_hub = package_quantity
            # Reset the csv iterator.
            packages_csv.seek(0)
            packages_reader = csv.reader(packages_csv)
            for row in packages_reader:
                # Skip the first row.
                if row[0] == 'ID':
                    continue
                # Create package record and add it to our package data.
                package = SoSPackage(row)
                SoSPackages.packages.insert(package.get_id(), package)
                # Sort special packages to be able to prioritize them.
                if package.get_deadline() != SoSPackage.NO_DEADLINE:
                    # These are packages need to be delivered before a certain time and will be prioritized.
                    SoSPackages.before_specified_time.append((package.get_id(), package.get_deadline()))
                if package.get_special_note():
                    # Add packages to with special notes to their respective group.
                    if package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.TRUCK_LIMITATION.value:
                        # These packages need to go on a particular truck.
                        SoSPackages.truck_restricted.append((package.get_id(), package.get_special_note()[1]))
                    if package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.DELAYED.value:
                        # These packages have been delayed.
                        SoSPackages.delayed.append((package.get_id(), package.get_special_note()[1]))
                    if package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.WRONG_ADDRESS.value:
                        # These (this since it's just one) packages have an incorrect address that will be corrected.
                        SoSPackages.wrong_address.append((package.get_id(), '10:20 am', '410 S State St', '84111'))
                    if package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.DELIVERED_WITH.value:
                        # These packages apparently need to go out together despite not all going to the same address.
                        SoSPackages.delivered_with.append((package.get_id(), package.get_special_note()[1]))
                else:
                    # All other packages will go in the pile of their respective destination.
                    SoSLocations.packages_to_locations.get(package.get_destination_lookup_id()).append(package.get_id())
