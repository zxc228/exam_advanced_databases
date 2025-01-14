#!/usr/bin/python
import sys

if __name__ == '__main__':
    current_year = None
    min_price = float('inf')
    max_price = float('-inf')
    supplier_min = None
    supplier_max = None

    for line in sys.stdin:
        fields = line.strip().split("\t")
        if len(fields) != 3:
            continue

        year, proveedor, price = fields
        try:
            year = int(year)
            price = float(price)
        except ValueError:
            continue  # Пропускаем ошибки преобразования

        if current_year is not None and year != current_year:
            # Выводим данные для предыдущего года
            print(f"{current_year}\t{min_price:.2f}\t{supplier_min}\t{max_price:.2f}\t{supplier_max}")

            # Обнуляем данные для нового года
            min_price = float('inf')
            max_price = float('-inf')
            supplier_min = None
            supplier_max = None

        current_year = year

        # Проверяем наименьшую цену
        if price < min_price:
            min_price = price
            supplier_min = proveedor

        # Проверяем наибольшую цену
        if price > max_price:
            max_price = price
            supplier_max = proveedor

    # Выводим последнюю строку (для последнего года)
    if current_year is not None:
        print(f"{current_year}\t{min_price:.2f}\t{supplier_min}\t{max_price:.2f}\t{supplier_max}")
