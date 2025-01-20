# Summary Advanced Databases
## MongoDB
### Основыне команды
- Для доступа к базе данных нужно использовать команду
    ```bash
    mongosh
    ```
- Показать доступные базы данных:
    ```bash
    show dbs
    ```
- Подключиться к базе данных (создаётся при записи данных):
    ```bash
    use myDatabase
    ```
- Показать коллекции в текущей бд
    ```bash
    show collections
    ```
- Удалить базу
    ```bash
    db.dropDatabase()
    ```
### Импорт и Экспорт 
- Импорт JSON файла
    ```bash
    mongoimport --db myDatabase --collection myCollection --file data.json --jsonArray
    ```
- Импорт из CSV файла
    ```bash 
    mongoimport --db myDatabase --collection myCollection --type csv --headerline --file data.csv
    ```
    --headerline = первая строка имена полей
- Экспорт коллекции в JSON
    ```bash
    mongoexport --db myDatabase --collection myCollection --out data.json --jsonArray
    ```
- Экспорт в CSV
    ```bash
    mongoexport --db myDatabase --collection myCollection --type csv --fields "field1,field2" --out data.csv
    ```
### CRUD
#### Создание
- insertOne(): вставляет один документ в коллекцию
    ```js
    db.collection.insertOne({ name: "John Doe" });
    ```
- insertMany(): вставляет массив документов
    ```js
    db.collection.insertMany([{ name: "Alice" }, { name: "Bob" }]);
    ```
#### Чтение
- find(): возвращает курсор с документами по критериям
    ```js
    db.collection.find({ age: { $gt: 25 } });
    ```
- findOne(): вовзращает первый документ по критериям
    ```js
    db.collection.findOne({ name: "Alice" });
    ```
#### Обновление
- updateOne(): Обновляет первый документ по критериям
    ```js
    db.collection.updateOne({ name: "Alice" }, { $set: { age: 30 } });
    ```
- updateMany(): Обновляет все документы
    ```js
    db.collection.updateMany({ age: { $lt: 18 } }, { $set: { status: "minor" } });
    ```
#### Удаление
- deleteOne(): Удалет первый документ по критериям
    ```js
    db.collection.deleteOne({ name: "Alice" });
    ```
- deleteMany(): Удаляет все документы по критериям
    ```js
    db.collection.deleteMany({ status: "inactive" });
    ```
### Аггрегация
1. $match это эквивалет WHERE
    
    синтаксис
    ```js
    { $match: { <field>: <condition> } }
    ```

    пример
    ```js
    db.students.aggregate([
    { $match: { "name.first": "John" } }
    ]);
    ```
2. $project проекция 


    синтаксис
    ```js
    { $project: { <field>: <expression>, ... } }
    ```


    пример
    ```js
    db.students.aggregate([
    { $project: { fullName: { $concat: ["$name.first", " ", "$name.last"] } } }
    ]);
    ```
3. $group группировка на основе выражения и вычисление аггрегатных значений

    синтаксис

    ```js
    { $group: { _id: <expression>, <field>: { <accumulator>: <expression> } } }
    ```

    пример
    ```js
    db.orders.aggregate([
    { $group: { _id: "$customerId", totalSpent: { $sum: "$amount" } } }
    ]);
    ```
4. $unwind разворчаивает массив в несколько документов


    синтаксис
    ```js
    { $unwind: <field> }
    ```

    пример
    ```js
    db.students.aggregate([
    { $unwind: "$subjects" }
    ]);
    ```
5. $sort 

    синтаксис
    ```js
    { $sort: { <field>: <order> } }
    ```
    - order: 1 возрастание -1 убывание
    пример
    ```js
    db.students.aggregate([
    { $sort: { age: -1 } }
    ]);
    ```
6. $limit ограничивает количество документов

    синтаксис
    ```js
    { $limit: <number> }
    ```

    пример
    ```js
    db.students.aggregate([
    { $limit: 5 }
    ]);
    ```
7. $skip пропускает указанное количество документов

    синтаксис
    ```js
    { $skip: <number> }
    ```

    пример 
    ```js
    db.students.aggregate([
    { $skip: 10 }
    ]);
    ```
8. $lookup это аналог join

    синтаксис
    ```js
    {
    $lookup: {
        from: <collection>,
        localField: <field>,
        foreignField: <field>,
        as: <output array>
    }
    }
    ```

    пример
    ```js
    db.orders.aggregate([
        { $lookup: {
            from: "customers",
            localField: "customerId",
            foreignField: "_id",
            as: "customerDetails"
        } }
    ]);
    ```
9. $geoNear Сортирует документы по близости к указанной географической точке

    синтаксис
    ```js
    {
        $geoNear: {
            near: { type: "Point", coordinates: [lng, lat] },
            distanceField: "<field>",
            maxDistance: <distance>,
            spherical: true
        }
    }
    ```

    пример 
    ```js
    db.places.aggregate([
        { $geoNear: {
            near: { type: "Point", coordinates: [-73.99279, 40.719296] },
            distanceField: "distance",
            spherical: true
        } }
    ]);

    ```
10. $out

    синтаксис
    ```js
    { $out: "<collection>" }
    ```

    пример

    ```js
    db.students.aggregate([
        { $match: { grade: { $gte: 5 } } },
        { $out: "passing_students" }
    ]);
    ```
11. $count оператор для подстчета кол-ва документов

    синтаксис
    ```js
    { $count: "<field>" }
    ```
    пример
    ```js
    db.students.aggregate([
    { $count: "totalDocuments" }
    ]);
    ```

### Аггрегаторные операторы 

Они используются вместе с $group
- $sum: Сумма значений.
- $avg: Среднее значение.
- $min, $max: Минимум и максимум.
- $push: Добавляет значения в массив.
- $addToSet: Добавляет уникальные значения в массив.

Пример
```js

db.orders.aggregate([
  { $group: {
    _id: "$customerId",
    totalSpent: { $sum: "$amount" },
    products: { $addToSet: "$product" }
  } }
]);
```

Выражения и операторы:

Арифметические операторы:
- $add, $subtract, $multiply, $divide, $mod.

Операторы сравнения:
- $eq, $gt, $lt, $gte, $lte, $ne, $in, $nin.

Логические операторы:
- $and, $or, $not, $nor.

Операторы для массивов:
- $size, $map, $filter, $reduce.

Условные операторы:
- $cond: "Если-иначе".
- $ifNull: Значение по умолчанию для null.

Операторы для строк:
- $concat, $substr, $toLower, $toUpper, $strcasecmp.

Операторы для дат:
- $year, $month, $dayOfMonth, $hour, $minute, $second.

    
## Redis
### Подключение
```bash
redis-cli
```
### Строки
Основные команды
- Установка/получение значения:
```bash
SET key value
GET key
```
- Установка со временем жизни
```bash 
SET key value EX 10 # Истекает через 10 секунд    
```
Инкременты/декременты
```bash
INCR key
DECR key
INCRBY key 5
DECRBY key 2
```

### Списки

Основные команды
- Добавление в список
```bash
LPUSH list value   # В начало
RPUSH list value   # В конец
```
- Извлечение
```bash
LPOP list          # Из начала
RPOP list          # Из конца
```
Диапазон элементов:
```bash
LRANGE list 0 -1   # Все элементы
```
### Множества

Основные команды
- Добавление/удаление
```bash
SADD set value
SREM set value
```

- Проверка наличия элемента
```bash
SISMEMBER set value
```


- Пересечения и объеденения
```bash
SINTER set1 set2       # Пересечение
SUNION set1 set2       # Объединение
```

### Упорядоченные множества  (Sorted Sets)

Особенности 
- Элементы имеют оценки (scores) для упорядочивания.

Основные команды
- Добавление 
```bash
ZADD zset score value
```
- Диапазоны
```bash
ZRANGE zset 0 -1 WITHSCORES  # Элементы с оценками
```
### Хэши
Основные команды
- Установка/получение
```bash
HSET hash key value
HGET hash key
```
- Все ключи и значения
```bash
HGETALL hash
```

### Управление ключами
- Установка времени жизни 
```bash
EXPIRE key seconds
```
- Проверка оставшегося времени
```bash
TTL key
```
- Удаление ключей
```bash
DEL key
```
### Транзакции
- Начало транзакции
```bash
MULTI
```
- Добавление команд 
```bash
SET key value
```
- Выполнение
```bash
EXEC
```

### Публикация/подписка
- Подписка
```bash
SUBSCRIBE channel
```
- Публикация
```bash
PUBLISH channel message
```
## Neo4J

0. Все удалить
    ```cypher
    MATCH(n)
    DETACH DELETE n;

1. Создание узлов
    
    Команда: CREATE
    
    Синтаксис:
    ```cypher
    CREATE (identifier:Label {property1: value1, property2: value2, ...})
    ```
    Пример:
    ```cypher
    CREATE (alice:Person {name: 'Alice', age: 30}),
        (newyork:City {name: 'New York'});
    ```
2. Создание связей
    
    Команда: CREATE
    
    Синтаксис:
    ```cypher
    MATCH (startNode:Label {property: value}), (endNode:Label {property: value})
    CREATE (startNode)-[:RELATIONSHIP_TYPE {property1: value1}]->(endNode)
    ```
    
    Пример:
    ```cypher
    MATCH (alice:Person {name: 'Alice'}), (newyork:City {name: 'New York'})
    CREATE (alice)-[:LIVES_IN]->(newyork);
    ```
3. Поиск узлов

    Команда: MATCH

    Синтаксис:

    ```cypher
    MATCH (identifier:Label {property: value})
    RETURN identifier;
    ```

    Пример:
    ```cypher
    MATCH (p:Person)
    RETURN p;
    ```

4. Поиск связей

    Команда: MATCH

    Синтаксис:

    ```cypher
    MATCH (startNode:Label)-[relationship:RELATIONSHIP_TYPE]->(endNode:Label)
    RETURN startNode, relationship, endNode;
    ```
    Пример:
    ```cypher
    MATCH (p:Person)-[r:LIVES_IN]->(c:City)
    RETURN p, r, c;
    ```
5. Фильтрация узлов

    Команда: WHERE

    Синтаксис:
    ```cypher
    MATCH (identifier:Label)
    WHERE condition
    RETURN identifier;
    ```
    Пример:
    ```cypher
    MATCH (p:Person)
    WHERE p.age > 30
    RETURN p.name AS Name, p.age AS Age;
    ```

6. Обновление свойств

    Команда: SET

    Синтаксис:

    ```cypher
    MATCH (identifier:Label {property: value})
    SET identifier.property = newValue
    RETURN identifier;
    ```
    Пример:
    ```cypher
    MATCH (eve:Person {name: 'Eve'})
    SET eve.age = 23
    RETURN eve.name AS Name, eve.age AS UpdatedAge;
    ```
7. Удаление связей

    Команда: DELETE

    Синтаксис:
    ```cypher
    MATCH (startNode:Label)-[relationship:RELATIONSHIP_TYPE]->(endNode:Label)
    DELETE relationship;
    ```
    Пример:
    ```cypher
    MATCH (bob:Person {name: 'Bob'})-[r:LIVES_IN]->(london:City {name: 'London'})
    DELETE r;
    ```
8. Удаление узлов

    Команда: DETACH DELETE

    Синтаксис:

    ```cypher
    MATCH (identifier:Label {property: value})
    DETACH DELETE identifier;
    ```
    Пример:

    ```cypher
    MATCH (dave:Person {name: 'Dave'})
    DETACH DELETE dave;
    ```
9. Уникальное создание (MERGE)

    Команда: MERGE

    Синтаксис:
    ```cypher
    MERGE (identifier:Label {property: value})
    RETURN identifier;
    ```
    Пример:

    ```cypher
    MERGE (a:Person {name: 'Alice', age: 30});
    ```
10. Ограничение количества и пропуск строк
    Команда: LIMIT, SKIP

    Синтаксис:
    ```cypher
    MATCH (identifier:Label)
    RETURN identifier
    LIMIT n
    SKIP m;
    ```
    Пример:
    ```cypher
    MATCH (p:Person)
    RETURN p
    LIMIT 2;
    ```
11. Агрегация

    Команда: COUNT, SUM, AVG, MAX, MIN

    Синтаксис:

    ```cypher
    MATCH (identifier:Label)
    RETURN AGGREGATE_FUNCTION(identifier.property);
    ```
    Пример:
    ```cypher
    MATCH (p:Person)
    RETURN avg(p.age);
    ```
12. Работа с коллекциями

    Команда: COLLECT

    Синтаксис:

    ```cypher
    MATCH (identifier:Label)
    RETURN collect(identifier.property);
    ```
    Пример:
    ```cypher
    MATCH (p:Person)
    RETURN collect(p.name);
    ```
13. Обновление схемы

    Команды: CREATE INDEX, DROP INDEX, CREATE CONSTRAINT, DROP CONSTRAINT

    Синтаксис:
    ```cypher
    CREATE INDEX FOR (identifier:Label) ON (identifier.property);
    DROP INDEX index_name;
   

    CREATE CONSTRAINT FOR (identifier:Label) REQUIRE identifier.property IS UNIQUE;
    DROP CONSTRAINT constraint_name;
    ```
    Пример:

    ```cypher
    CREATE INDEX FOR (p:Person) ON (p.name);
    ```
14. Сортировка результатов

    Команда: ORDER BY
    
    Синтаксис:
    ```cypher
    MATCH (identifier:Label)
    RETURN identifier
    ORDER BY identifier.property ASC/DESC;
    ```
    Пример:
    ```cypher
    MATCH (p:Person)
    RETURN p
    ORDER BY p.age DESC;
    ```
## MapReduce or BigData

### Extension to databases: Big Data
**Что такое Big Data?**

**Big Data** – термин для описания любого типа структурированных, полуструктурированных или неструктурированных данных, которые имеют:
- Большой объем (Volume): Необходимость хранения данных в различных местах (кластер).
- Разнообразие (Variety): Источники информации (например, изображения, видео, социальные сети).
- Скорость (Velocity): Высокая скорость создания и обработки данных (включая реальное время).

Задачи Big Data (3Vs):
1.	Объем (Volume):
- Огромные объемы данных требуют распределенного хранения.
- Можно применять несколько аналитических техник для анализа данных.
2.	Разнообразие (Variety):
- Данные поступают из множества источников и форматов.
- Необходимо сохранять данные в их исходном формате для предотвращения потерь.
3.	Скорость (Velocity):
- Скорость хранения данных без предварительной обработки критична.
- Традиционные методы анализа не подходят для централизованной обработки данных.

Другие вызовы Big Data:
- Переменность (Variability): Непостоянство данных.
- Правдивость (Veracity): Качество хранимой информации.
- Сложность (Complexity): Хранение взаимосвязанных данных для полной аналитической картины.

## Cassandra
### Архитектура записи (Write Path Flow):
1. Memtable
- Для каждой CQL-таблицы и KeySpace создаётся Memtable.
- Назначение:
    - Хранение запросов записи до их переноса на диск.
    - Данные в Memtable доступны для чтения до их записи на диск.
- Функции:
    - Периодический сброс: Данные перемещаются в новые SSTables на жёстком диске, а соответствующие записи в Commitlog помечаются как "flushed".
2. SSTable
- Характеристики:
    - SSTables неизменяемы: данные только накапливаются.
    - Каждая Memtable создаёт новую SSTable при сбросе.
- Компактация:
    - Периодически все SSTables сливаются в одну, чтобы исключить дублирующиеся записи.
### Архитектура чтения (Read Path Flow):
1. Процесс чтения
- Cassandra ищет данные как в Memtables, так и в SSTables по указанному ключу партиции.
- Результат объединяется через процесс merge, используя записи с последними временными метками.
2. Ускорение запросов
- Используются фильтры и промежуточные кеши:
    - Row Cache: Хранит результаты последних запросов, чтобы избежать повторного слияния данных.
    - Key Cache: Сохраняет позиции последних запросов для быстрого доступа к данным.
    - Partition Summary: Индекс в памяти для ускорения доступа к данным в Partition Index.
    - Bloom Filter: Указывает, содержится ли первичный ключ в SSTable (есть вероятность ложных срабатываний, но исключены ложные отрицания).
### Компоненты и их функции:
1. Row Cache
- Сохраняет результаты последних запросов.
- Особенности:
    - По умолчанию отключён.
    - Содержимое кеша периодически сохраняется на диск для восстановления после перезагрузки.
2. Bloom Filter
- Назначение:
    - Вероятностная структура данных, которая проверяет наличие первичного ключа в SSTable.
- Характеристики:
    - Ложные срабатывания возможны, ложные отрицания отсутствуют.
    - Уровень ложных срабатываний настраивается (чем ниже, тем больше памяти используется).
3. Key Cache
- Сохраняет позиции последних запросов.
- Преимущества:
    - Снижает необходимость доступа к таблицам партиций для определения позиций в SSTable.
    - Содержимое кеша сохраняется на диск для восстановления после перезагрузки.
4. Partition Summary и Partition Index
- Partition Summary:
    - Индекс в памяти для быстрого доступа к данным в Partition Index.
- Partition Index:
    - Полный набор позиций для каждого ключа партиции в SSTable.
### Общие принципы Cassandra:
1. Распределённая архитектура
- Данные распределяются между несколькими узлами для повышения отказоустойчивости и производительности.
- Каждый узел может выполнять как чтение, так и запись.
2. Репликация и согласованность
- Cassandra использует модель репликации данных для обеспечения высокой доступности.
- Настраивается уровень согласованности (например, QUORUM, ONE).
3. Компактация данных
- Компактация SSTable удаляет дубликаты и улучшает производительность чтения.
### Основные компоненты производительности:
1. Memtable и SSTable:
- Memtable хранит данные во временной памяти.
- SSTable используется для долговременного хранения.
2. Кеши:

- Row Cache ускоряет повторные запросы.
- Key Cache снижает нагрузку на индексные таблицы.
3. Bloom Filter:

- Уменьшает затраты на поиск данных.
4. Компактация:

- Устраняет дублирование данных для улучшения чтения.