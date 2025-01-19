#!/usr/bin/python
import sys

if __name__ == '__main__':
    current_key = None  # Current key (Supplier\tYear-Month)
    total_price = 0  # Total sales price
    count = 0  # Number of records (for average calculation)

    for line in sys.stdin:  # Read lines from standard input
        fields = line.strip().split("\t")  # Split line by tab
        
        if len(fields) != 3:  # Check data correctness (should be 3 columns)
            continue

        proveedor, mes_anio, precio = fields  # Extract data: Supplier, Year-Month, Price
        
        try:
            precio = float(precio)  # Convert price to number
        except ValueError:
            continue  # Skip line if conversion error
        
        key = f"{proveedor}\t{mes_anio}"  # Form key for grouping

        if current_key and key != current_key:  # If current key changed (new group)
            avg_price = total_price / count if count > 0 else 0  # Вычисляем среднее
            print(f"{current_key}\t{avg_price:.2f}")  # Выводим результат
            total_price = 0  # Сбрасываем сумму
            count = 0  # Сбрасываем счетчик

        current_key = key  # Обновляем текущий ключ
        total_price += precio  # Добавляем цену к общей сумме
        count += 1  # Увеличиваем счетчик

    # Обрабатываем последний ключ (последняя группа данных)
    if current_key:
        avg_price = total_price / count if count > 0 else 0  # Вычисляем среднее
        print(f"{current_key}\t{avg_price:.2f}")  # Выводим результат
