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
            origen = fields[6].strip()  # Город отправки
            destino = fields[7].strip()  # Город получения
            
            print(f"{origen}\tout\t1")  # Исходящая отправка
            print(f"{destino}\tin\t1")  # Входящая отправка
        except ValueError:
            continue  # Пропускаем строки с ошибками
