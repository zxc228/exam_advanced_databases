#!/usr/bin/python
import sys

if __name__ == '__main__':
    current_key = None
    shipping_types = set()  # Unique shipping types

    for line in sys.stdin:
        fields = line.strip().split("\t")
        if len(fields) != 3:
            continue

        proveedor, mes_anio, tipo_envio = fields
        try:
            tipo_envio = int(tipo_envio)
        except ValueError:
            continue  # Skip lines with conversion errors

        key = f"{proveedor}\t{mes_anio}"

        if current_key and key != current_key:
            # Output the result for the previous key
            print(f"{current_key}\t{','.join(map(str, sorted(shipping_types)))}")
            shipping_types.clear()

        current_key = key
        shipping_types.add(tipo_envio)

    # Output the last result
    if current_key:
        print(f"{current_key}\t{','.join(map(str, sorted(shipping_types)))}")