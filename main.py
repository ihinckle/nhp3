import csv
from src.classes.SoSHashTable import SoSHashTable
from src.classes.SoSPackage import SoSPackage


package_quantity = None
packages = None

with open('resources/packages.csv') as packages_csv:
    packages_reader = csv.reader(packages_csv)
    package_quantity = sum(1 for row in packages_reader) - 1
    packages = SoSHashTable(package_quantity)
    for row in packages_reader:
        if row[0] == 'ID':
            continue
        package = SoSPackage(row)
        packages.insert(package.get_id(), package)
