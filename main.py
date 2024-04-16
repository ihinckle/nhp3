import csv

from src.classes.SoSHashTable import SoSHashTable
from src.classes.SoSPackage import SoSPackage
from src.classes.SoSTruck import SoSTruck
from src.utils.LocationsUtils import LocationsUtils


def main():
    locations, packages_sorted = LocationsUtils.set_up_locations_table()
    truck_restricted = []
    delayed = []
    wrong_address = []
    delivered_with = []
    truck_1: SoSTruck = SoSTruck()
    truck_2: SoSTruck = SoSTruck()
    truck_3: SoSTruck = SoSTruck()

    with open('resources/packages.csv') as packages_csv:
        packages_reader = csv.reader(packages_csv)
        package_quantity = sum(1 for row in packages_reader) - 1
        packages = SoSHashTable(package_quantity)
        packages_csv.seek(0)
        packages_reader = csv.reader(packages_csv)
        for row in packages_reader:
            if row[0] == 'ID':
                continue
            package = SoSPackage(row)
            packages.insert(package.get_id(), package)
            if package.get_special_note():
                if package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.TRUCK_LIMITATION.value:
                    truck_restricted.append((package.get_id(), package.get_special_note()[1]))
                if package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.DELAYED.value:
                    delayed.append((package.get_id(), package.get_special_note()[1]))
                if package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.WRONG_ADDRESS.value:
                    wrong_address.append(package.get_id())
                if package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.DELIVERED_WITH.value:
                    delivered_with.append((package.get_id(), package.get_special_note()[1]))
            else:
                packages_sorted.get(package.get_address() + package.get_zip()).append(package.get_id())

    for item in truck_restricted:
        truck: SoSTruck = None
        match item[1]:
            case '1':
                truck = truck_1
            case '2':
                truck = truck_2
            case '3':
                truck = truck_3
        package: SoSPackage = packages.get(item[0])
        truck.load(package)
        load_more(truck, packages_sorted.get(package.get_destination_id()))


def load_more(truck: SoSTruck, packages: list):
    if packages.len() < 1:
        return
    for packageId in packages:
        truck.load()



main()
