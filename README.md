# Анализ зарплат программистов по вакансиям с HeadHunter и SuperJob #


Скрипт собирает вакансии с платформ HeadHunter и SuperJob, анализирует предлагаемые зарплаты и рассчитывает среднюю зарплату для популярных языков программирования.

## Требования ##

Перед запуском убедитесь, что у вас установлен ```Python``` версии 3.8 или выше.

Необходимые зависимости указаны в файле ```requirements.txt```:
```
requests==2.32.3
python-dotenv==1.0.1
terminaltables==3.1.10
```

Установите их командой:
```
pip install -r requirements.txt
```

## Настройка API ключа ##

Для работы с SuperJob необходимо указать API-ключ.
Вы можете передать его через аргумент командной строки или через переменную окружения ```SJ_KEY```.

## Запуск ##
```
python main.py --sj_key=<ВАШ_API_КЛЮЧ>
```

Или, если API-ключ задан в переменной окружения:
```
python main.py
```

## Как работает скрипт ##

### Входные данные: ###

* API-ключ SuperJob (указывается через аргумент командной строки --sj_key или переменную окружения SJ_KEY)

* Список языков программирования для анализа (задан в коде)

* Данные о вакансиях с HeadHunter и SuperJob

## Процесс работы: ##

1. Отправка запросов к API HeadHunter и SuperJob для поиска вакансий по каждому языку программирования.

2. Извлечение информации о зарплатах из полученных данных.

3. Расчет средней зарплаты на основе минимальных и максимальных значений зарплат.

4. Формирование таблицы с итоговыми данными.


## Вывод данных ##

Скрипт собирает вакансии в Москве, рассчитывает средние зарплаты по самым популярным языкам программирования:

* Python

* Java

* JavaScript

* C++

* C#

* PHP

* Go

* Swift

* Kotlin

* Ruby

После выполнения программы вы увидите таблицы с данными о средней зарплате для каждого языка программирования из источников HeadHunter и SuperJob.

**Средние зарплаты по языкам программирования (HeadHunter)**:

| Язык       | Найдено вакансий | Обработано вакансий | Средняя зарплата (руб.) |
|------------|----------------|-------------------|-------------------|
| Python     | 250            | 200               | 180000            |
| Java       | 300            | 250               | 190000            |
| JavaScript | 280            | 230               | 170000            |
| C++        | 220            | 180               | 175000            |
| C#         | 200            | 150               | 160000            |
| PHP        | 150            | 120               | 140000            |
| Go         | 120            | 100               | 195000            |
| Swift      | 100            | 80                | 185000            |
| Kotlin     | 90             | 70                | 180000            |
| Ruby       | 80             | 60                | 165000            |

**Средние зарплаты по языкам программирования (SuperJob)**:

| Язык       | Найдено вакансий | Обработано вакансий | Средняя зарплата (руб.) |
|------------|----------------|-------------------|-------------------|
| Python     | 220            | 180               | 175000            |
| Java       | 280            | 240               | 185000            |
| JavaScript | 260            | 210               | 165000            |
| C++        | 210            | 170               | 170000            |
| C#         | 180            | 140               | 155000            |
| PHP        | 140            | 110               | 135000            |
| Go         | 100            | 90                | 190000            |
| Swift      | 90             | 70                | 180000            |
| Kotlin     | 85             | 65                | 175000            |
| Ruby       | 75             | 55                | 160000            |




