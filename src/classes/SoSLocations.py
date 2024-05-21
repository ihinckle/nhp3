import csv

from src.classes.SoSHashTable import SoSHashTable
from src.classes.SoSLocation import SoSLocation


class SoSLocations:
    locations: SoSHashTable
    packages_to_locations: SoSHashTable
    location_distances: list[list] = []

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
                SoSLocations.locations.insert(SoSLocations.create_destination_id(location.get_address() + location.get_zip()), location)
                SoSLocations.packages_to_locations.insert(SoSLocations.create_destination_id(location.get_address() + location.get_zip()), [])
        with open('resources/location_distances.csv') as distances_csv:
            distances_reader = csv.reader(distances_csv)
            for row in distances_reader:
                SoSLocations.location_distances.append(row)


    @staticmethod
    def create_destination_id(string: str) -> str:
        return string.replace(' ', '')

    @staticmethod
    def lookup_distance(current_location_id, destination_id):
        lookup_check = SoSLocations.location_distances[current_location_id][destination_id]
        if lookup_check != '':
            return lookup_check
        else:
            return SoSLocations.location_distances[destination_id][current_location_id]
