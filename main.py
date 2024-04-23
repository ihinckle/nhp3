from src.classes.SoSLocations import SoSLocationsfrom src.classes.SoSPackage import SoSPackagefrom src.classes.SoSPackages import SoSPackagesfrom src.classes.SoSTruck import SoSTruckdef main():    SoSLocations.initialize()    SoSPackages.initialize()    truck_1: SoSTruck = SoSTruck(1)    truck_2: SoSTruck = SoSTruck(2)    truck_3: SoSTruck = SoSTruck(3)    load_truck(truck_1)    load_truck(truck_2)    # while not truck_1.is_full():    #     if len(SoSPackages.before_specified_time) > 0:    #         package_id, time = SoSPackages.before_specified_time.pop(0)    #         package: SoSPackage = SoSPackages.packages.get(package_id)    #         if package.get_special_note() and package.get_special_note()[0] == SoSPackage.SPECIAL_NOTE_TYPE.DELAYED.value:    #             continue    #         truck_1.load(package)    #         load_more(truck_1, SoSLocations.packages_to_locations.get(package.get_destination_id()))    #     else:    #         break    # for package_id, truck_number in SoSPackages.truck_restricted:    #     truck: SoSTruck | None = None    #     match truck_number:    #         case '1':    #             truck = truck_1    #         case '2':    #             truck = truck_2    #         case '3':    #             truck = truck_3    #     package: SoSPackage = SoSPackages.packages.get(package_id)    #     if truck:    #         truck.load(package)    #         load_more(truck, SoSLocations.packages_to_locations.get(package.get_destination_id()))    # for package_id, package_ids in SoSPackages.delivered_with:    truck_1.print_cargo()    truck_1.print_destinations()    truck_2.print_cargo()    truck_2.print_destinations()    print(len(SoSPackages.truck_restricted))    print(len(SoSPackages.before_specified_time))def load_truck(truck: SoSTruck):    packages_to_load = []    if len(SoSPackages.truck_restricted) > 0:        filtered = filter(lambda x: x[1] == truck.get_truck_number(), SoSPackages.truck_restricted)        filtered_list = list(filtered)        mapped = map(lambda x: x[0], filtered_list)        mapped_list = list(mapped)        packages_to_load.extend(mapped_list)    if len(SoSPackages.before_specified_time) > 0:        mapped = map(lambda x: x[0], SoSPackages.before_specified_time)        mapped_list = list(mapped)        packages_to_load.extend(mapped_list)    while not truck.is_full() and len(packages_to_load) > 0:        package: SoSPackage = SoSPackages.packages.get(packages_to_load.pop())        if package.get_special_note() and package.get_special_note()[0] in [SoSPackage.SPECIAL_NOTE_TYPE.DELAYED.value, SoSPackage.SPECIAL_NOTE_TYPE.WRONG_ADDRESS.value]:            continue        truck.load(package)        load_more(truck, SoSLocations.packages_to_locations.get(package.get_destination_id()))def load_more(truck: SoSTruck, packages: list):    if len(packages) < 1:        return    while not truck.is_full():        if len(packages) > 0:            package = SoSPackages.packages.get(packages.pop(0))            truck.load(package)        else:            breakmain()