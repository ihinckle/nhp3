import csv

from src.classes.SoSHashTable import SoSHashTable
from src.classes.SoSLocation import SoSLocation


class SoSLocations:
    locations: SoSHashTable
    packages_to_locations: SoSHashTable
    location_distances: list[list] = []

    # Initialize class.
    @staticmethod
    def initialize():
        with open('resources/locations.csv') as locations_csv:
            # Count how many records exist to create a perfect sized HashTable.
            locations_quantity = len(locations_csv.readlines()) - 1
            SoSLocations.locations = SoSHashTable(locations_quantity)
            SoSLocations.packages_to_locations = SoSHashTable(locations_quantity)
            # Reset the iterator on the csv.
            locations_csv.seek(0)
            locations_reader = csv.reader(locations_csv)
            for row in locations_reader:
                # Skip the first row of the csv.
                if row[0] == 'ID':
                    continue
                # Create location record
                location = SoSLocation(row)
                # Create lookup index and insert location record.
                SoSLocations.locations.insert(SoSLocations.create_destination_lookup_id(location.get_address() + location.get_zip()), location)
                # Create a HashTable where we can sort packages according to delivery address.
                # This will allow for less loops through the package data.
                SoSLocations.packages_to_locations.insert(SoSLocations.create_destination_lookup_id(location.get_address() + location.get_zip()), [])
        with open('resources/location_distances.csv') as distances_csv:
            distances_reader = csv.reader(distances_csv)
            for row in distances_reader:
                # Create the distances lookup matrix.
                SoSLocations.location_distances.append(row)

    # Creates a location lookup id that can be used in any class to ensure the same results.
    @staticmethod
    def create_destination_lookup_id(string: str) -> str:
        return string.replace(' ', '')

    # Lookup the distance between two location ids.
    @staticmethod
    def lookup_distance(current_location_id, destination_id):
        current_location_id = int(current_location_id)
        destination_id = int(destination_id)
        # Lookup distance.
        lookup_check = SoSLocations.location_distances[current_location_id][destination_id]
        # If a distance is found then we are on the wrong half of the matrix.
        # Swap the ids and return the result.
        if lookup_check != '':
            return lookup_check
        else:
            return SoSLocations.location_distances[destination_id][current_location_id]
