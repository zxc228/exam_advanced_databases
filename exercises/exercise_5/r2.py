#!/usr/bin/python
import sys

if __name__ == '__main__':
    current_key = None  # Текущий ключ (Поставщик\tГод-Месяц)
    total_price = 0  # Суммарная стоимость продаж
    count = 0  # Количество записей (для расчета среднего)

    for line in sys.stdin:  # Читаем строки из стандартного ввода
        fields = line.strip().split("\t")  # Разделяем строку по табуляции
        
        if len(fields) != 3:  # Проверяем корректность данных (должно быть 3 колонки)
            continue

        proveedor, mes_anio, precio = fields  # Извлекаем данные: Поставщик, Год-Месяц, Цена
        
        try:
            precio = float(precio)  # Преобразуем цену в число
        except ValueError:
            continue  # Если ошибка преобразования, пропускаем строку
        
        key = f"{proveedor}\t{mes_anio}"  # Формируем ключ для группировки

        if current_key and key != current_key:  # Если текущий ключ изменился (новая группа)
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
