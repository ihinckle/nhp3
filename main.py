import csv
from src.classes.SoSHashTable import SoSHashTable
from src.classes.SoSLocation import SoSLocation
from src.classes.SoSPackage import SoSPackage


packages = None
locations = None

# with open('resources/locations.csv') as locations_csv:
#     locations_reader = csv.reader(locations_csv)
#     locations_quantity = sum(1 for row in locations_reader) - 1
#     locations = SoSHashTable(locations_quantity)
#     for row in locations_reader:
#         if row[0] == 'ID':
#             continue
#         location = SoSLocation(row)
#         locations.insert(location.address+location.zip, location)

with open('resources/packages.csv') as packages_csv:
    packages_reader = csv.reader(packages_csv)
    package_quantity = 40
    packages = SoSHashTable(package_quantity)
    for row in packages_reader:
        if row[0] == 'ID':
            continue
        package = SoSPackage(row)
        packages.insert(package.get_id(), package)

for package in packages:
    print(package.get_id())
