#!/usr/bin/python
import sys

if __name__ == '__main__':
    total_price = 0  # Общая сумма продаж с доставкой типа 1
    count = 0  # Количество таких продаж

    for line in sys.stdin:
        fields = line.strip().split("\t")
        if len(fields) != 2:
            continue

        _, price = fields  # Нам не нужен ключ, только значение
        try:
            price = float(price)
        except ValueError:
            continue  # Пропускаем ошибки преобразования

        total_price += price
        count += 1

    # Вычисляем и выводим среднюю плотность продаж
    avg_density = total_price / count if count > 0 else 0
    print(f"Average sales density of deivery type 1: {avg_density:.2f}")
