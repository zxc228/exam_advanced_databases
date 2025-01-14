class RouteManager:

    def __init__(self, graph_manager):
        """
        Initializes the RouteManager with a reference to the GraphManager.
        """
        self.graph_manager = graph_manager

    def find_cheapest_route(self, origin, destination):
        """
        Finds the cheapest route between two nodes.
        Considers loading at the origin, unloading at the destination, and switching transports at intermediate points.
        
        :param origin: Name of the starting node.
        :param destination: Name of the destination node.
        :return: List of nodes in the route, total cost, total time, and route details.
        """
        graph_data = self.get_graph_data()
        if origin not in graph_data or destination not in graph_data:
            raise ValueError("Origin or destination not found in the graph.")

        if graph_data[destination]["node"]._properties["type"] == "Intermediate":
            raise ValueError("Intermediate platforms cannot be selected as delivery points.")

        from logistics.utils import transport_params

        costs = {node: float('inf') for node in graph_data}
        times = {node: float('inf') for node in graph_data}
        previous_nodes = {node: None for node in graph_data}
        path_details = {node: None for node in graph_data}
        visited = set()
        costs[origin] = 0
        times[origin] = 0

        from heapq import heappush, heappop
        priority_queue = []
        heappush(priority_queue, (0, origin, None))  # (cost, node, previous transport)

        while priority_queue:
            current_cost, current_node, current_transport = heappop(priority_queue)

            if current_node in visited:
                continue
            visited.add(current_node)

            if current_node == destination:
                break

            for edge in graph_data[current_node]['edges']:
                next_node = edge['to_node']
                edge_info = edge['edge_info']
                transport_type = edge_info.type
                distance = edge_info._properties['distance']
                load_time = 0
                unload_time = 0

                if current_transport and current_transport != transport_type:
                    unload_time = transport_params[current_transport]['load_unload_time']
                    load_time = transport_params[transport_type]['load_unload_time']
                elif current_transport is None:
                    load_time = transport_params[transport_type]['load_unload_time']

                cost_per_100km = transport_params[transport_type]['cost_per_100km']
                time_per_100km = transport_params[transport_type]['time_per_100km']
                travel_cost = (distance / 100) * cost_per_100km
                travel_time = (distance / 100) * time_per_100km
                total_time = travel_time + load_time + unload_time

                new_cost = current_cost + travel_cost
                new_time = times[current_node] + total_time

                if new_cost < costs[next_node]:
                    costs[next_node] = new_cost
                    times[next_node] = new_time
                    previous_nodes[next_node] = (current_node, transport_type)
                    path_details[next_node] = {
                        'from': current_node,
                        'to': next_node,
                        'transport': transport_type,
                        'distance': distance,
                        'load_time': load_time,
                        'unload_time': unload_time,
                        'travel_time': travel_time,
                        'total_time': total_time,
                        'total_cost': travel_cost
                    }
                    heappush(priority_queue, (new_cost, next_node, transport_type))

        path = []
        current = destination
        detailed_path = []
        while current:
            path.append(current)
            if path_details[current]:
                detailed_path.append(path_details[current])
            current = previous_nodes[current][0] if current in previous_nodes and previous_nodes[current] else None
        path.reverse()
        detailed_path.reverse()

        if detailed_path:
            last_segment = detailed_path[-1]
            last_transport = last_segment['transport']
            unload_time = transport_params[last_transport]['load_unload_time']
            last_segment['unload_time'] += unload_time
            last_segment['total_time'] += unload_time
            times[destination] += unload_time

        return path, costs[destination], times[destination], detailed_path

    def find_fastest_route(self, origin, destination):
        """
        Finds the fastest route by time between two nodes.
        Considers loading at the origin, unloading at the destination, and switching transports at intermediate points.
        
        :param origin: Name of the starting node.
        :param destination: Name of the destination node.
        :return: List of nodes in the route, total time, total cost, and route details.
        """
        graph_data = self.get_graph_data()
        if origin not in graph_data or destination not in graph_data:
            raise ValueError("Origin or destination not found in the graph.")
        if graph_data[destination]["node"]._properties["type"] == "Intermediate":
            raise ValueError("Intermediate platforms cannot be selected as delivery points.")

        from logistics.utils import transport_params

        distances = {node: float('inf') for node in graph_data}
        costs = {node: float('inf') for node in graph_data}
        previous_nodes = {node: None for node in graph_data}
        path_details = {node: None for node in graph_data}
        visited = set()
        distances[origin] = 0
        costs[origin] = 0

        from heapq import heappush, heappop
        priority_queue = []
        heappush(priority_queue, (0, origin, None))  # (time, node, previous transport)

        while priority_queue:
            current_time, current_node, current_transport = heappop(priority_queue)

            if current_node in visited:
                continue
            visited.add(current_node)

            if current_node == destination:
                break

            for edge in graph_data[current_node]['edges']:
                next_node = edge['to_node']
                edge_info = edge['edge_info']
                transport_type = edge_info.type
                distance = edge_info._properties['distance']
                load_time = 0
                unload_time = 0

                if current_transport and current_transport != transport_type:
                    unload_time = transport_params[current_transport]['load_unload_time']
                    load_time = transport_params[transport_type]['load_unload_time']
                elif current_transport is None:
                    load_time = transport_params[transport_type]['load_unload_time']

                time_per_100km = transport_params[transport_type]['time_per_100km']
                travel_time = (distance / 100) * time_per_100km
                total_segment_time = travel_time + load_time + unload_time

                cost_per_100km = transport_params[transport_type]['cost_per_100km']
                travel_cost = (distance / 100) * cost_per_100km

                new_time = current_time + total_segment_time
                new_cost = costs[current_node] + travel_cost

                if new_time < distances[next_node]:
                    distances[next_node] = new_time
                    costs[next_node] = new_cost
                    previous_nodes[next_node] = (current_node, transport_type)
                    path_details[next_node] = {
                        'from': current_node,
                        'to': next_node,
                        'transport': transport_type,
                        'distance': distance,
                        'load_time': load_time,
                        'unload_time': unload_time,
                        'travel_time': travel_time,
                        'total_time': total_segment_time,
                        'total_cost': travel_cost
                    }
                    heappush(priority_queue, (new_time, next_node, transport_type))

        path = []
        current = destination
        detailed_path = []
        while current:
            path.append(current)
            if path_details[current]:
                detailed_path.append(path_details[current])
            current = previous_nodes[current][0] if current in previous_nodes and previous_nodes[current] else None
        path.reverse()
        detailed_path.reverse()

        if detailed_path:
            last_segment = detailed_path[-1]
            last_transport = last_segment['transport']
            unload_time = transport_params[last_transport]['load_unload_time']
            last_segment['unload_time'] += unload_time
            last_segment['total_time'] += unload_time
            distances[destination] += unload_time

        return path, costs[destination], distances[destination], detailed_path

    def find_delivery_options(self, origin, destination, start_time):
        """Finds available delivery options (Same_day, One_day, Economy) for a given route."""
        from datetime import timedelta

        cheapest_route = self.find_cheapest_route(origin, destination)
        fastest_route = self.find_fastest_route(origin, destination)

        deadline_same_day = start_time.replace(hour=19, minute=0, second=0) - timedelta(hours=1)
        deadline_one_day = deadline_same_day.replace(hour=14, minute=0, second=0) + timedelta(days=1)

        delivery_options = {'Same_day': None, 'One_day': None, 'Economy': None}

        economy_time = start_time + timedelta(minutes=cheapest_route[2])
        if economy_time <= deadline_same_day:
            delivery_options['Same_day'] = cheapest_route
        elif economy_time <= deadline_one_day:
            delivery_options['One_day'] = cheapest_route
        else:
            delivery_options['Economy'] = cheapest_route

        fastest_time = start_time + timedelta(minutes=fastest_route[2])
        if fastest_time <= deadline_same_day and (delivery_options['Same_day'] is None or fastest_route[1] < delivery_options['Same_day'][1]):
            delivery_options['Same_day'] = fastest_route
        if fastest_time <= deadline_one_day and (delivery_options['One_day'] is None or fastest_route[1] < delivery_options['One_day'][1]):
            delivery_options['One_day'] = fastest_route
        if delivery_options['Economy'] is None or fastest_route[1] < delivery_options['Economy'][1]:
            delivery_options['Economy'] = fastest_route

        used_routes = set()
        for key in ['Same_day', 'One_day', 'Economy']:
            if delivery_options[key] is not None:
                route_key = tuple(delivery_options[key][0])
                if route_key in used_routes:
                    delivery_options[key] = None
                else:
                    used_routes.add(route_key)

        return {key: value for key, value in delivery_options.items() if value is not None}

    def get_graph_data(self):
        """Retrieves the entire graph data structure."""
        graph_data = {}
        with self.graph_manager.driver.session() as session:
            result = session.run("MATCH (n) RETURN n")
            for record in result:
                node_id = record["n"]["id"]
                graph_data[node_id] = {
                    "node": self.graph_manager.get_node_info(node_id),
                    "edges": []
                }
                edge_result = session.run("""
                    MATCH (a {id: $node_id})-[r]->(b)
                    RETURN r, b.id as to_node
                """, node_id=node_id)
                for edge_record in edge_result:
                    edge_info = edge_record["r"]
                    to_node = edge_record["to_node"]
                    graph_data[node_id]["edges"].append({
                        "to_node": to_node,
                        "edge_info": edge_info
                    })
        return graph_data

    def route_output(self, route):
        """Formats and prints detailed route information."""
        nodes, total_cost, total_time, details = route

        print("Route:")
        print(" -> ".join(nodes))
        print(f"\nTotal route cost: {total_cost:.2f} units")
        print(f"Total route time: {total_time:.2f} minutes\n")
        print(f"Total route distance: {sum(segment['distance'] for segment in details)} km")
        print(f"Average delivery speed: {sum(segment['distance'] for segment in details) / (total_time / 60):.2f} km/h")
        print(f"Transport changes: {len([segment for i, segment in enumerate(details[:-1]) if segment['transport'] != details[i + 1]['transport']])}")

        print("Route details:")
        for segment in details:
            print(
                f"From {segment['from']} to {segment['to']}:\n"
                f"  - Transport: {segment['transport']}\n"
                f"  - Distance: {segment['distance']} km\n"
                f"  - Unload time: {segment['unload_time']} minutes\n"
                f"  - Load time: {segment['load_time']} minutes\n"
                f"  - Travel time: {segment['travel_time']:.2f} minutes\n"
                f"  - Total segment time: {segment['total_time']:.2f} minutes\n"
                f"  - Segment cost: {segment['total_cost']:.2f} units\n"
            )
