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
            tipo_envio = int(fields[2].strip())  # Shipping type
            precio = float(fields[8].strip())  # Sale price
            
            if tipo_envio == 1:  # Filter only sales with shipping type 1
                print(f"Density\t{precio}")
        except ValueError:
            continue  # Skip lines with errors
