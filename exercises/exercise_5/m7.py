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
            tipo_envio = int(fields[2].strip())  # Тип доставки
            
            # Разбираем дату (формат: "10/11/2003")
            dia, mes, anio = fecha.split("/")
            mes_anio = f"{anio}-{mes}"

            print(f"{proveedor}\t{mes_anio}\t{tipo_envio}")  # Выводим "Поставщик\tГод-Месяц\tТип доставки"
        except ValueError:
            continue  # Пропускаем строки с ошибками
