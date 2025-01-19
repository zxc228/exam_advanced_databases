#!/usr/bin/python
import sys

if __name__ == '__main__':
    for i, line in enumerate(sys.stdin):
        if i == 0:  # Skip header
            continue
        fields = line.strip().split("\t")

        if len(fields) != 9:  # Check number of columns
            continue
        
        try:
            origen = fields[6].strip()  # Origin city
            destino = fields[7].strip()  # Destination city
            precio = float(fields[8].strip())  # Sale price

            print(f"{origen}\tout\t{precio}")  # Revenue from origin city
            print(f"{destino}\tin\t{precio}")  # Revenue to destination city
        except ValueError:
            continue  # Skip lines with errors
