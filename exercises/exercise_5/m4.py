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
            
            # Определяем стоимость доставки
            if tipo_envio == 1:
                shipping_cost = 10
            elif tipo_envio == 2:
                shipping_cost = 5
            elif tipo_envio == 3:
                shipping_cost = 3
            else:
                continue  # Пропускаем неизвестные типы

            print(f"{proveedor}\t{anio}\t{shipping_cost}")  # Выводим "Поставщик\tГод\tСтоимость доставки"
        except ValueError:
            continue  # Пропускаем строки с ошибками
