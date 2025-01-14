#!/usr/bin/python
import sys
from collections import defaultdict

if __name__ == '__main__':
    city_balance = defaultdict(lambda: {"in": 0, "out": 0})  # {город: {"in": сумма, "out": сумма}}

    for line in sys.stdin:
        fields = line.strip().split("\t")
        if len(fields) != 3:
            continue

        city, direction, price = fields
        try:
            price = float(price)
        except ValueError:
            continue  # Пропускаем ошибки преобразования

        city_balance[city][direction] += price

    # Вычисляем и выводим баланс для каждого города
    for city, balances in city_balance.items():
        balance = balances["out"] - balances["in"]
        print(f"{city}\t{balance:.2f}")
