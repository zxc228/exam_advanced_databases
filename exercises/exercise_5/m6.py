#!/usr/bin/python
import sys

if __name__ == '__main__':
    for i, line in enumerate(sys.stdin):
        if i == 0:  # Пропуск заголовка
            continue
        fields = line.strip().split("\t")

        if len(fields) != 9:  # Проверяем количество колонок
            continue
        
        try:
            tipo_envio = int(fields[2].strip())  # Тип доставки
            precio = float(fields[8].strip())  # Стоимость продажи
            
            if tipo_envio == 1:  # Фильтруем только продажи с доставкой типа 1
                print(f"Плотность\t{precio}")
        except ValueError:
            continue  # Пропускаем строки с ошибками
