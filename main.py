import csv

from src.classes.SoSHashTable import SoSHashTable
from src.classes.SoSPackage import SoSPackage
from src.classes.SoSPackages import SoSPackages
from src.classes.SoSTruck import SoSTruck
from src.utils.LocationsUtils import LocationsUtils


def main():
    locations, packages_sorted = LocationsUtils.set_up_locations_table()
    truck_1: SoSTruck = SoSTruck()
    truck_2: SoSTruck = SoSTruck()
    truck_3: SoSTruck = SoSTruck()

    SoSPackages.get_packages(packages_sorted)
    for package in SoSPackages.packages:
        print(package)

    # for item in truck_restricted:
    #     truck: SoSTruck | None = None
    #     match item[1]:
    #         case '1':
    #             truck = truck_1
    #         case '2':
    #             truck = truck_2
    #         case '3':
    #             truck = truck_3
    #     package: SoSPackage = packages.get(item[0])
    #     if truck:
    #         truck.load(package)
#           load_more(truck, packages_sorted.get(package.get_destination_id()))
#
#
# def load_more(truck: SoSTruck, packages: list):
#     if packages.len() < 1:
#         return
#     for packageId in packages:
#         truck.load()


main()
