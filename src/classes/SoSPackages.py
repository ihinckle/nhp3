import csv

from src.classes.SoSHashTable import SoSHashTable
from src.classes.SoSPackage import SoSPackage


class SoSPackages:
    packages: SoSHashTable
    truck_restricted: list[tuple] = []
    delayed: list[tuple] = []
    wrong_address: list[str] = []
    delivered_with: list[tuple] = []
    packages_sorted: SoSHashTable

    @staticmethod
    def get_packages(packages_sorted):
        SoSPackages.packages_sorted = packages_sorted

        with open('resources/packages.csv') as packages_csv:
            package_quantity = len(packages_csv.readlines()) - 1
            SoSPackages.packages = SoSHashTable(package_quantity)
            packages_csv.seek(0)
            packages_reader = csv.reader(packages_csv)
            for row in packages_reader:
                if row[0] == 'ID':
                    continue
                package = SoSPackage(row)
                SoSPackages.packages.insert(package.get_id(), package)
                if package.get_special_note():
                    if package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.TRUCK_LIMITATION.value:
                        SoSPackages.truck_restricted.append((package.get_id(), package.get_special_note()[1]))
                    if package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.DELAYED.value:
                        SoSPackages.delayed.append((package.get_id(), package.get_special_note()[1]))
                    if package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.WRONG_ADDRESS.value:
                        SoSPackages.wrong_address.append(package.get_id())
                    if package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.DELIVERED_WITH.value:
                        SoSPackages.delivered_with.append((package.get_id(), package.get_special_note()[1]))
                else:
                    SoSPackages.packages_sorted.get(package.get_address() + package.get_zip()).append(package.get_id())
