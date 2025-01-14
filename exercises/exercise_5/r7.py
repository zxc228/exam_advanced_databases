#!/usr/bin/python
import sys

if __name__ == '__main__':
    current_key = None
    shipping_types = set()  # Уникальные типы доставок

    for line in sys.stdin:
        fields = line.strip().split("\t")
        if len(fields) != 3:
            continue

        proveedor, mes_anio, tipo_envio = fields
        try:
            tipo_envio = int(tipo_envio)
        except ValueError:
            continue  # Пропускаем ошибки преобразования

        key = f"{proveedor}\t{mes_anio}"

        if current_key and key != current_key:
            print(f"{current_key}\t{','.join(map(str, sorted(shipping_types)))}")
            shipping_types.clear()

        current_key = key
        shipping_types.add(tipo_envio)

    # Выводим последний результат
    if current_key:
        print(f"{current_key}\t{','.join(map(str, sorted(shipping_types)))}")
