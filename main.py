import csv
import re
from src.classes.SoSHashTable import SoSHashTable
from src.classes.SoSLocation import SoSLocation
from src.classes.SoSPackage import SoSPackage


packages = None
locations = None
packages_sorted = None
truck_restricted = []

with open('resources/locations.csv') as locations_csv:
    locations_reader = csv.reader(locations_csv)
    locations_quantity = sum(1 for row in locations_reader) - 1
    locations = SoSHashTable(locations_quantity)
    packages_sorted = SoSHashTable(locations_quantity)
    locations_csv.seek(0)
    locations_reader = csv.reader(locations_csv)
    for row in locations_reader:
        if row[0] == 'ID':
            continue
        location = SoSLocation(row)
        locations.insert(location.get_address()+location.get_zip(), location)
        packages_sorted.insert(location.get_address()+location.get_zip(), [])

for location in locations:
    print(location.get_location())


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
            if package.get_special_note()[0] == package.SPECIAL_NOTE_TYPE.TRUCK_LIMITATION.value:
                truck_restricted.append((package.get_id(), package.get_special_note()[1]))
        else:
            packages_sorted.get(package.get_address()+package.get_zip()).append(package.get_id())

for package in packages:
    print(package.get_id())

print(truck_restricted)
