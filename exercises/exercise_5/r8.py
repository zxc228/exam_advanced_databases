#!/usr/bin/python
import sys
from collections import defaultdict

if __name__ == '__main__':
    route_counts = defaultdict(lambda: defaultdict(int))  # {год: {маршрут: кол-во отправок}}

    for line in sys.stdin:
        fields = line.strip().split("\t")
        if len(fields) != 3:
            continue

        year, route, count = fields
        try:
            year = int(year)
            count = int(count)
        except ValueError:
            continue  # Пропускаем ошибки преобразования

        route_counts[year][route] += count  # Считаем количество отправок

    # Определяем маршрут с максимальным трафиком в каждом году
    for year in sorted(route_counts.keys()):
        top_route = max(route_counts[year].items(), key=lambda x: x[1])  # Находим маршрут с макс. отправками
        print(f"{year}\t{top_route[0]}\t{top_route[1]}")
