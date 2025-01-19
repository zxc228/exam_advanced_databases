#!/usr/bin/python
import sys

if __name__ == '__main__':
    total_price = 0  # Total sum of sales with delivery type 1
    count = 0  # Count of such sales

    for line in sys.stdin:
        fields = line.strip().split("\t")
        if len(fields) != 2:
            continue

        _, price = fields  # We only need the value, not the key
        try:
            price = float(price)
        except ValueError:
            continue  # Skip lines with conversion errors

        total_price += price
        count += 1

    # Calculate and print the average sales density
    avg_density = total_price / count if count > 0 else 0
    print(f"Average sales density of delivery type 1: {avg_density:.2f}")