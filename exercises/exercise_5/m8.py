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
            fecha = fields[5].strip()  # Дата продажи
            origen = fields[6].strip()  # Город отправки
            destino = fields[7].strip()  # Город доставки
            
            # Разбираем дату (формат: "10/11/2003")
            dia, mes, anio = fecha.split("/")

            route = f"{origen}→{destino}"

            print(f"{anio}\t{route}\t1")  # Выводим "Год\tМаршрут\t1"
        except ValueError:
            continue  # Пропускаем строки с ошибками
