from logistics.graph import GraphManager
from logistics.routes import RouteManager
from logistics.fleet import FleetManager
from logistics.package import PackageManager
from config import Config
import logistics.utils as utils
from datetime import datetime, timedelta
import pprint

if __name__ == "__main__":
    # Initialize the graph
    graph_manager = GraphManager(
        uri='bolt://localhost:7687',
        user=Config.user,
        password=Config.password,
        transport_params=utils.transport_params,
        nodes=utils.nodes,
        edges=utils.edges
    )
    graph_manager.reset_graph()
    graph_manager.setup_graph()

    # Initialize managers
    route_manager = RouteManager(graph_manager)
    fleet_manager = FleetManager()
    package_manager = PackageManager(fleet_manager, time_threshold=10)

    # Test routes
    start_time = datetime(2024, 1, 1, 8, 0, 0)

    # 1) Test routes via RouteManager
    print("Example Routes (Same_day):")
    routes_1 = route_manager.find_delivery_options("Bilbao", "Palma", start_time)
    routes_2 = route_manager.find_delivery_options("Barcelona", "Zaragoza", start_time)
    routes_3 = route_manager.find_delivery_options("Valencia", "Alicante", start_time)
    routes_4 = route_manager.find_delivery_options("Madrid", "Seville", start_time)

    print("Route Bilbao -> Palma:")
    print('Available delivery types:', routes_1.keys())
    
    print('Route Barcelona -> Zaragoza:')
    print('Available delivery types:', routes_2.keys())

    print('Route Valencia -> Alicante:')
    print('Available delivery types:', routes_3.keys())
    
    print('Route Madrid -> Seville:')
    print('Available delivery types:', routes_4.keys())

    route_manager.route_output(routes_1["Same_day"])
    route_manager.route_output(routes_2["Same_day"])
    route_manager.route_output(routes_3["Same_day"])
    route_manager.route_output(routes_4["Same_day"])

    # 2) Register packages
    pkg_id_1 = package_manager.register_package(routes_1, "Same_day", start_time)
    pkg_id_2 = package_manager.register_package(routes_2, "Same_day", start_time)
    pkg_id_3 = package_manager.register_package(routes_2, "Same_day", start_time + timedelta(minutes=5))
    pkg_id_4 = package_manager.register_package(routes_3, "Same_day", start_time)
    pkg_id_5 = package_manager.register_package(routes_4, "Same_day", start_time + timedelta(minutes=3))

    # Apply delays
    package_manager.apply_delay(pkg_id_1, 10)

    # Assign vehicles for initial segments
    package_manager.assign_initial_vehicles()

    # Generate the final delivery schedule
    schedule = package_manager.create_schedule()

    print("\nFinal Delivery Schedule:")
    pprint.pprint(schedule)

    # Pretty-formatted schedule output
    print("\nFormatted Schedule by Segments:")
    for pkg_id, pkg_sched in schedule.items():
        print(f"\nPackage {pkg_id}:")
        print(f"  Delivery Type: {pkg_sched['delivery_type']}")
        print(f"  Final Start Time: {pkg_sched['final_start_time']}")
        print(f"  Delay: {pkg_sched['delay']} minutes")
        print(f"  Route: {' -> '.join(pkg_sched['route'])}")

        for i, seg in enumerate(pkg_sched["detailed_segments"], 1):
            print(f"  Segment {i}:")
            print(f"    From: {seg['from']} to {seg['to']} via {seg['transport']}")
            print(f"    Segment Start Time: {seg['segment_start']}")
            print(f"    Loading: {seg['load_start']} ({seg['load_time']} mins)")
            print(f"    Departure: {seg['depart_time']}, Arrival: {seg['arrival_time']}")
            print(f"    Unloading: {seg['unload_time']} mins, Segment End: {seg['segment_end']}")
            print(f"    Vehicle ID: {seg['vehicle_id']}")
            print(f"    Segment Cost: {seg['total_cost']}, Total Time: {seg['total_time']} mins\n")
