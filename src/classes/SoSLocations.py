import csv

from src.classes.SoSHashTable import SoSHashTable
from src.classes.SoSLocation import SoSLocation


class SoSLocations:
    locations: SoSHashTable
    packages_to_locations: SoSHashTable

    @staticmethod
    def initialize():
        with open('resources/locations.csv') as locations_csv:
            locations_quantity = len(locations_csv.readlines()) - 1
            SoSLocations.locations = SoSHashTable(locations_quantity)
            SoSLocations.packages_to_locations = SoSHashTable(locations_quantity)
            locations_csv.seek(0)
            locations_reader = csv.reader(locations_csv)
            for row in locations_reader:
                if row[0] == 'ID':
                    continue
                location = SoSLocation(row)
                SoSLocations.locations.insert(location.get_address() + location.get_zip(), location)
                SoSLocations.packages_to_locations.insert(location.get_address() + location.get_zip(), [])
