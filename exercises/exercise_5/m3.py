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
            proveedor = fields[1].strip()  # Поставщик
            fecha = fields[5].strip()  # Дата продажи
            precio = float(fields[8].strip())  # Цена продажи
            
            # Разбираем дату (формат: "10/11/2003")
            dia, mes, anio = fecha.split("/")
            
            print(f"{proveedor}\t{anio}\t{precio}")  # Выводим "Поставщик\tГод\tЦена"
        except ValueError:
            continue  # Пропускаем строки с ошибками
