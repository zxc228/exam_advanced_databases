#!/usr/bin/python
import sys
from collections import defaultdict

if __name__ == '__main__':
    route_counts = defaultdict(lambda: defaultdict(int))  # {year: {route: shipment_count}}

    for line in sys.stdin:
        fields = line.strip().split("\t")
        if len(fields) != 3:
            continue

        year, route, count = fields
        try:
            year = int(year)
            count = int(count)
        except ValueError:
            continue  # Skip lines with conversion errors

        route_counts[year][route] += count  # Count the number of shipments

    # Determine the route with the maximum traffic for each year
    for year in sorted(route_counts.keys()):
        top_route = max(route_counts[year].items(), key=lambda x: x[1])  # Find the route with the max shipments
        print(f"{year}\t{top_route[0]}\t{top_route[1]}")