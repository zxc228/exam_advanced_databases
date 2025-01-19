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
            proveedor = fields[1].strip()  # Supplier
            fecha = fields[5].strip()  # Sale date
            precio = float(fields[8].strip())  # Sale price
            
            # Parse date (format: "10/11/2003")
            dia, mes, anio = fecha.split("/")
            
            print(f"{anio}\t{proveedor}\t{precio}")  # Output "Year\tSupplier\tPrice"
        except ValueError:
            continue  # Skip lines with errors
