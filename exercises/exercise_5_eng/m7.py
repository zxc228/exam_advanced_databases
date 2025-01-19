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
            tipo_envio = int(fields[2].strip())  # Shipping type
            
            # Parse date (format: "10/11/2003")
            dia, mes, anio = fecha.split("/")
            mes_anio = f"{anio}-{mes}"

            print(f"{proveedor}\t{mes_anio}\t{tipo_envio}")  # Output "Supplier\tYear-Month\tShipping type"
        except ValueError:
            continue  # Skip lines with errors
