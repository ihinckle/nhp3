# Created by Isaac Hinckley (000636849)import sysfrom datetime import datetimefrom src.classes.SoSLocations import SoSLocationsfrom src.classes.SoSPackage import SoSPackagefrom src.classes.SoSPackages import SoSPackagesfrom src.classes.SoSTruck import SoSTruckfrom src.classes.SoSTrucks import SoSTrucks# Simulation steps.def simulate_deliveries():    # Import and set up location data.    SoSLocations.initialize()    # Import and set up package data.    SoSPackages.initialize()    # Initialize department trucks    truck_1: SoSTruck = SoSTrucks.truck_1    truck_2: SoSTruck = SoSTrucks.truck_2    # Only two drivers showed up for work today. Truck 3 will not be used.    truck_3: SoSTruck = SoSTrucks.truck_3    # Perform work until packages are gone.    while SoSPackages.packages_at_hub > 0:        # No use of asynchronous systems. Simulation will drive one truck at a time.        active_truck: SoSTruck = determine_which_truck(truck_1, truck_2)        # Load the active truck.        active_truck.load_truck()        # Send the truck to work.        active_truck.perform_deliveries()# Checks the truck clocks against each other. Whichever truck has the earliest time will be the designated active truck.# Defaults to truck 1 if both clocks match.def determine_which_truck(truck_1, truck_2):    return truck_1 if truck_1.get_time() <= truck_2.get_time() else truck_2def pick_option():    print('Pick option (any other input assumes option 1)')def print_package_info(package: SoSPackage):    print('Package-', package.get_id(),          ' : Status-', package.get_delivery_status_readable(),          ' : Time-', package.get_delivered_time().time(),          ' : Deadline-', package.get_deadline(),          ' : Truck-', package.get_on_truck(),          ' : Destination-', package.get_address(), ', ', package.get_zip(), ' ', package.get_city(),          ' : Weight-', package.get_weight())def end_of_day_report():    print('Total miles travelled: ', SoSTrucks.truck_1.get_miles_traveled()+SoSTrucks.truck_2.get_miles_traveled())    pick_option()    print('1 - All packages')    print('2 - Specific package')    print('3 - Back')    print('0 - Quit')    user_input = input('Option: ')    match user_input:        case '2':            package_to_query = input('Enter package ID: ')            package = SoSPackages.packages.get(package_to_query)            if package != -1:                print_package_info(package)                end_of_day_report()        case '3':            user_interface()        case '0':            sys.exit('Goodbye')        case _:            SoSPackages.packages.reset_iterator()            for package in SoSPackages.packages:                print_package_info(package)            end_of_day_report()def determine_package_status(package, report_datetime):    if package.get_loaded_time() > report_datetime:        return 'At Hub'    elif package.get_delivered_time() > report_datetime:        return 'En Route'    else:        return 'Delivered'def specific_package_report():    package_id = input('Enter package ID: ')    package: SoSPackage = SoSPackages.packages.get(package_id)    if package == -1:        print('Invalid package ID')        return    report_time = input('Enter report time (format hh:mm am/pm): ')    try:        report_time_datetime = datetime.strptime(report_time, '%H:%M %p')    except ValueError:        print('Invalid report time')        return    print('Package: ', package.get_id())    print('Status: ', determine_package_status(package, report_time_datetime))    if determine_package_status(package, report_time_datetime) == 'En Route':        print('On Truck: ', package.get_on_truck())    elif determine_package_status(package, report_time_datetime) == 'Delivered':        print('By Truck: ', package.get_on_truck())    if package.get_id() == '9' and report_time_datetime < datetime.strptime('10:20 am', '%H:%M %p'):        print('Destination: 300 State St, 84103 Salt Lake City')    else:        print('Destination: ', package.get_address(), ', ', package.get_zip(), ' ', package.get_city())    print('Deadline: ', package.get_deadline())    print('Weight: ', package.get_weight())    user_interface()def packages_en_route_report():    report_time = input('Enter report time (format hh:mm am/pm): ')    try:        report_time_datetime = datetime.strptime(report_time, '%H:%M %p')    except ValueError:        print('Invalid report time')        return    SoSPackages.packages.reset_iterator()    packages_en_route = filter(lambda x: determine_package_status(x, report_time_datetime) == 'En Route', SoSPackages.packages)    packages_en_route_list = list(packages_en_route)    print('Truck 1:')    for package in list(filter(lambda x: x.get_on_truck() == '1', packages_en_route_list)):        print('Package: ', package.get_id(), ' : En route on truck ', package.get_on_truck())    print('Truck 2:')    for package in list(filter(lambda x: x.get_on_truck() == '2', packages_en_route_list)):        print('Package: ', package.get_id(), ' : En route on truck ', package.get_on_truck())    user_interface()def user_interface():    pick_option()    print('1 - End of day data')    print('2 - Specific package at time')    print('3 - Packages en route at given time')    print('0 - Quit')    user_input = input('Option: ')    match user_input:        case '0':            sys.exit('Goodbye')        case '2':            specific_package_report()        case '3':            packages_en_route_report()        case _:            end_of_day_report()simulate_deliveries()user_interface()