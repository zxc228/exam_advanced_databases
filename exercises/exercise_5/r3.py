#!/usr/bin/python
import sys

if __name__ == '__main__':
    current_supplier = None
    previous_year = None
    previous_revenue = None
    current_year = None
    current_revenue = 0

    for line in sys.stdin:
        fields = line.strip().split("\t")
        if len(fields) != 3:
            continue

        proveedor, year, price = fields
        try:
            year = int(year)
            price = float(price)
        except ValueError:
            continue  # Пропускаем ошибки преобразования

        if current_supplier and proveedor != current_supplier:
            # Вычисляем рост для последнего года
            if previous_year is not None and previous_revenue is not None:
                growth = ((current_revenue - previous_revenue) / previous_revenue) * 100 if previous_revenue > 0 else 0
                print(f"{current_supplier}\t{current_year}\t{growth:.2f}%")

            # Сбрасываем данные для нового поставщика
            previous_year = None
            previous_revenue = None
            current_revenue = 0

        current_supplier = proveedor
        current_year = year

        # Если это новый год, обновляем предыдущие данные
        if previous_year is not None and previous_year != current_year:
            growth = ((current_revenue - previous_revenue) / previous_revenue) * 100 if previous_revenue > 0 else 0
            print(f"{current_supplier}\t{current_year}\t{growth:.2f}%")
            previous_revenue = current_revenue

        previous_year = current_year
        previous_revenue = current_revenue
        current_revenue += price

    # Обрабатываем последний поставщик/год
    if previous_year is not None and previous_revenue is not None:
        growth = ((current_revenue - previous_revenue) / previous_revenue) * 100 if previous_revenue > 0 else 0
        print(f"{current_supplier}\t{current_year}\t{growth:.2f}%")
