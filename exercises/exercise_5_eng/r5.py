#!/usr/bin/python
import sys

if __name__ == '__main__':
    current_year = None
    min_price = float('inf')  # Initialize minimum price as infinity
    max_price = float('-inf')  # Initialize maximum price as negative infinity
    supplier_min = None  # Supplier with the minimum price
    supplier_max = None  # Supplier with the maximum price

    for line in sys.stdin:
        fields = line.strip().split("\t")
        if len(fields) != 3:
            continue

        year, proveedor, price = fields
        try:
            year = int(year)
            price = float(price)
        except ValueError:
            continue  # Skip lines with conversion errors

        if current_year is not None and year != current_year:
            # Output data for the previous year
            print(f"{current_year}\t{min_price:.2f}\t{supplier_min}\t{max_price:.2f}\t{supplier_max}")

            # Reset data for the new year
            min_price = float('inf')
            max_price = float('-inf')
            supplier_min = None
            supplier_max = None

        current_year = year

        # Check for the lowest price
        if price < min_price:
            min_price = price
            supplier_min = proveedor

        # Check for the highest price
        if price > max_price:
            max_price = price
            supplier_max = proveedor

    # Output the last row (for the last year)
    if current_year is not None:
        print(f"{current_year}\t{min_price:.2f}\t{supplier_min}\t{max_price:.2f}\t{supplier_max}")