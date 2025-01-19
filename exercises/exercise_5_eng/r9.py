#!/usr/bin/python
import sys
from collections import defaultdict

if __name__ == '__main__':
    city_counts = defaultdict(lambda: {"in": 0, "out": 0})  # {city: {"in": count, "out": count}}

    for line in sys.stdin:
        fields = line.strip().split("\t")
        if len(fields) != 3:
            continue

        city, direction, count = fields
        try:
            count = int(count)
        except ValueError:
            continue  # Skip lines with conversion errors

        city_counts[city][direction] += count

    # Find the city with the highest traffic
    top_city = None
    max_traffic = 0

    for city, counts in city_counts.items():
        total_traffic = counts["in"] + counts["out"]
        if total_traffic > max_traffic:
            top_city = city
            max_traffic = total_traffic

    # Output the city with the highest traffic
    if top_city:
        print(f"{top_city}\t{max_traffic}")