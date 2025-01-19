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
            
            # Determine shipping cost
            if tipo_envio == 1:
                shipping_cost = 10
            elif tipo_envio == 2:
                shipping_cost = 5
            elif tipo_envio == 3:
                shipping_cost = 3
            else:
                continue  # Skip unknown types

            print(f"{proveedor}\t{anio}\t{shipping_cost}")  # Output "Supplier\tYear\tShipping cost"
        except ValueError:
            continue  # Skip lines with errors
