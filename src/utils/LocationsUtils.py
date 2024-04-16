import csv

from src.classes.SoSHashTable import SoSHashTable
from src.classes.SoSLocation import SoSLocation


class LocationsUtils:
    @staticmethod
    def set_up_locations_table():
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
                locations.insert(location.get_address() + location.get_zip(), location)
                packages_sorted.insert(location.get_address() + location.get_zip(), [])
            return locations, packages_sorted
