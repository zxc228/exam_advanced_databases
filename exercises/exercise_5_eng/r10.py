#!/usr/bin/python
import sys
from collections import defaultdict

if __name__ == '__main__':
    city_balance = defaultdict(lambda: {"in": 0, "out": 0})  # {city: {"in": total, "out": total}}

    for line in sys.stdin:
        fields = line.strip().split("\t")
        if len(fields) != 3:
            continue

        city, direction, price = fields
        try:
            price = float(price)
        except ValueError:
            continue  # Skip lines with conversion errors

        city_balance[city][direction] += price

    # Calculate and output the balance for each city
    for city, balances in city_balance.items():
        balance = balances["out"] - balances["in"]
        print(f"{city}\t{balance:.2f}")