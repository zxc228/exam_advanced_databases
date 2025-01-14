class FleetManager:
    def __init__(self):
        """
        Initializes FleetManager.
        vehicles: Dictionary { (transport_type, tuple(route)): vehicle_id }
        next_vehicle_id: Counter for assigning unique vehicle IDs.
        """
        self.vehicles = {}  # {(transport_type, (route)): vehicle_id}
        self.next_vehicle_id = 1

    def get_vehicle_for_route(self, transport_type, route):
        """
        Returns the vehicle ID for a given transport type and route.
        If the vehicle is not already registered, a new one is created.
        
        :param transport_type: Type of transport (e.g., 'railway', 'aerial', etc.)
        :param route: List of nodes in the route.
        :return: vehicle_id (int)
        """
        key = (transport_type, tuple(route))
        if key not in self.vehicles:
            vehicle_id = self.next_vehicle_id
            self.vehicles[key] = vehicle_id
            self.next_vehicle_id += 1
        else:
            vehicle_id = self.vehicles[key]
        return vehicle_id
