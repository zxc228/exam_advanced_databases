#!/usr/bin/python
import sys
from collections import defaultdict

if __name__ == '__main__':
    supplier_shipping = defaultdict(lambda: defaultdict(int))  # {год: {поставщик: сумма_расходов}}

    for line in sys.stdin:
        fields = line.strip().split("\t")
        if len(fields) != 3:
            continue

        proveedor, year, shipping_cost = fields
        try:
            year = int(year)
            shipping_cost = int(shipping_cost)
        except ValueError:
            continue  # Пропускаем ошибки преобразования

        supplier_shipping[year][proveedor] += shipping_cost  # Суммируем затраты

    # Обрабатываем данные по каждому году
    for year in sorted(supplier_shipping.keys()):
        sorted_suppliers = sorted(supplier_shipping[year].items(), key=lambda x: x[1], reverse=True)[:3]  # Топ-3
        for proveedor, total_cost in sorted_suppliers:
            print(f"{year}\t{proveedor}\t{total_cost}")
