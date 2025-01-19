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
            
            print(f"{origen}\tout\t1")  # Outgoing shipment
            print(f"{destino}\tin\t1")  # Incoming shipment
        except ValueError:
            continue  # Skip lines with errors
