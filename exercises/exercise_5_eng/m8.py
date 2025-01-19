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
            fecha = fields[5].strip()  # Sale date
            origen = fields[6].strip()  # Origin city
            destino = fields[7].strip()  # Destination city
            
            # Parse date (format: "10/11/2003")
            dia, mes, anio = fecha.split("/")

            route = f"{origen}→{destino}"

            print(f"{anio}\t{route}\t1")  # Output "Year\tRoute\t1"
        except ValueError:
            continue  # Skip lines with errors
