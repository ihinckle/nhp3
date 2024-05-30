# Created by Isaac Hinckley (000636849)from src.classes.SoSLocations import SoSLocationsfrom src.classes.SoSPackages import SoSPackagesfrom src.classes.SoSTruck import SoSTruck# Simulation steps.def main():    # Import and set up location data.    SoSLocations.initialize()    # Import and set up package data.    SoSPackages.initialize()    # Initialize department trucks    truck_1: SoSTruck = SoSTruck(1)    truck_2: SoSTruck = SoSTruck(2)    # Only two drivers showed up for work today. Truck 3 will not be used.    truck_3: SoSTruck = SoSTruck(3)    # Perform work until packages are gone.    while SoSPackages.packages_at_hub > 0:        # No use of asynchronous systems. Simulation will drive one truck at a time.        active_truck: SoSTruck = determine_which_truck(truck_1, truck_2)        # Load the active truck.        active_truck.load_truck()        # Send the truck to work.        active_truck.perform_deliveries()# Checks the truck clocks against each other. Whichever truck has the earliest time will be the designated active truck.# Defaults to truck 1 if both clocks match.def determine_which_truck(truck_1, truck_2):    return truck_1 if truck_1.get_time() <= truck_2.get_time() else truck_2main()