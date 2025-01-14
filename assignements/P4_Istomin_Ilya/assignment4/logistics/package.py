class PackageManager:
    def __init__(self, fleet_manager, time_threshold=10):
        """
        :param fleet_manager: Instance of FleetManager.
        :param time_threshold: Time threshold in minutes to consider packages "simultaneous."
        """
        self.fleet_manager = fleet_manager
        self.packages = {}
        self.package_id_counter = 1
        self.time_threshold = time_threshold

        self.full_route_map = {}  # {tuple(route): [(package_id, start_time), ...]}
        self.package_groups = {}  # {package_id: {"full_route_shared": bool, "group_vehicle_id": int or None}}

    def register_package(self, delivery_options, delivery_type, start_time):
        """
        Registers a single package.
        """
        if delivery_type not in delivery_options:
            raise ValueError(f"Delivery type '{delivery_type}' not available.")

        route_data = delivery_options[delivery_type]
        route = route_data[0]
        segments = route_data[3]

        pkg_id = self.package_id_counter
        self.package_id_counter += 1

        self.packages[pkg_id] = {
            "delivery_type": delivery_type,
            "route": route,
            "segments": segments,
            "start_time": start_time,
            "delivery_options": delivery_options,
            "delay": 0,
            "initial_vehicle_id": None
        }

        route_key = tuple(route)
        if route_key not in self.full_route_map:
            self.full_route_map[route_key] = []
        self.full_route_map[route_key].append((pkg_id, start_time))

        self.package_groups[pkg_id] = {"full_route_shared": False, "group_vehicle_id": None}

        return pkg_id

    def apply_delay(self, package_id, delay_minutes):
        """
        Applies a delay to a specific package.
        """
        if package_id not in self.packages:
            raise KeyError(f"Package ID {package_id} not found.")

        from datetime import timedelta
        self.packages[package_id]["delay"] = delay_minutes
        self.packages[package_id]["start_time"] += timedelta(minutes=delay_minutes)

        route_key = tuple(self.packages[package_id]["route"])
        for i, (p_id, st) in enumerate(self.full_route_map[route_key]):
            if p_id == package_id:
                self.full_route_map[route_key][i] = (package_id, self.packages[package_id]["start_time"])
                break

    def assign_initial_vehicles(self):
        """
        Assigns vehicles for the first segment of packages with the same initial segment and similar start times.
        Also checks for packages that share the full route and assigns them one group vehicle.
        """

        first_segments_map = {}  # {(transport_type, (from, to)): [(package_id, start_time), ...]}

        for pkg_id, pkg_data in self.packages.items():
            first_segment = pkg_data["segments"][0]
            transport_type = first_segment["transport"]
            seg_route = (first_segment["from"], first_segment["to"])
            key = (transport_type, seg_route)
            if key not in first_segments_map:
                first_segments_map[key] = []
            first_segments_map[key].append((pkg_id, pkg_data["start_time"]))

        for key, pkg_list in first_segments_map.items():
            pkg_list.sort(key=lambda x: x[1])
            assigned_vehicles = []
            for (pkg_id, start_time) in pkg_list:
                assigned = False
                for (veh_id, ref_time) in assigned_vehicles:
                    diff = abs((start_time - ref_time).total_seconds() / 60.0)
                    if diff <= self.time_threshold:
                        self.packages[pkg_id]["initial_vehicle_id"] = veh_id
                        assigned = True
                        break
                if not assigned:
                    vehicle_id = self.fleet_manager.get_vehicle_for_route(key[0], list(key[1]))
                    self.packages[pkg_id]["initial_vehicle_id"] = vehicle_id
                    assigned_vehicles.append((vehicle_id, start_time))

        for route_key, pkg_list in self.full_route_map.items():
            if len(pkg_list) < 2:
                continue
            pkg_list.sort(key=lambda x: x[1])

            base_time = pkg_list[0][1]
            full_group = True
            for _, st_time in pkg_list[1:]:
                diff = abs((st_time - base_time).total_seconds() / 60.0)
                if diff > self.time_threshold:
                    full_group = False
                    break

            if full_group:
                first_pkg_id = pkg_list[0][0]
                group_vehicle_id = self.packages[first_pkg_id]["initial_vehicle_id"]
                for (p_id, _) in pkg_list:
                    self.package_groups[p_id]["full_route_shared"] = True
                    self.package_groups[p_id]["group_vehicle_id"] = group_vehicle_id

    def create_schedule(self):
        """
        Creates the final schedule.
        Assigns vehicles for all segments, using the group vehicle if packages share the full route.
        """
        from datetime import timedelta
        schedule = {}

        for pkg_id, pkg_data in self.packages.items():
            final_start_time = pkg_data["start_time"]
            segments = pkg_data["segments"]
            current_time = final_start_time
            detailed_segments = []

            full_group = self.package_groups[pkg_id]["full_route_shared"]
            group_vehicle_id = self.package_groups[pkg_id]["group_vehicle_id"]
            initial_vehicle_id = pkg_data["initial_vehicle_id"]

            for i, seg in enumerate(segments):
                transport_type = seg["transport"]
                segment_route = [seg["from"], seg["to"]]

                if full_group:
                    vehicle_id = group_vehicle_id
                else:
                    if i == 0:
                        vehicle_id = initial_vehicle_id
                    else:
                        vehicle_id = self.fleet_manager.get_vehicle_for_route(transport_type, segment_route)

                segment_start = current_time
                load_start = segment_start
                load_end = load_start + timedelta(minutes=seg["load_time"])
                depart_time = load_end
                travel_end = depart_time + timedelta(minutes=seg["travel_time"])
                arrival_time = travel_end
                unload_end = arrival_time + timedelta(minutes=seg["unload_time"])
                segment_end = unload_end
                current_time = segment_end

                detailed_segments.append({
                    "from": seg["from"],
                    "to": seg["to"],
                    "transport": seg["transport"],
                    "segment_start": segment_start,
                    "load_start": load_start,
                    "depart_time": depart_time,
                    "arrival_time": arrival_time,
                    "segment_end": segment_end,
                    "vehicle_id": vehicle_id,
                    "load_time": seg["load_time"],
                    "unload_time": seg["unload_time"],
                    "travel_time": seg["travel_time"],
                    "total_time": seg["total_time"],
                    "total_cost": seg["total_cost"]
                })

            schedule[pkg_id] = {
                "delivery_type": pkg_data["delivery_type"],
                "final_start_time": pkg_data["start_time"],
                "delay": pkg_data["delay"],
                "route": pkg_data["route"],
                "detailed_segments": detailed_segments
            }

        return schedule
