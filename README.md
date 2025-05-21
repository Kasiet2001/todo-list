 # ToDo API на FastAPI

Простой REST API для управления задачами (ToDo), реализованный с использованием FastAPI и SQLite.

---

## Оглавление

- [Описание](#описание)
- [Технологии](#технологии)
- [Установка](#установка)
- [Запуск](#запуск)
- [Примеры запросов](#примеры-запросов)

---

## Описание

Это базовое ToDo-приложение с возможностью создавать, получать, обновлять и удалять задачи. Используется FastAPI для быстрого и удобного создания API, а SQLite — для хранения данных.

---

## Технологии

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

---

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://https://github.com/Kasiet2001/todo-list
   cd todo_list
   
2. Создайте виртуальное окружение:
    ```bash
   source venv/bin/activate   #Linux/macOS
   venv\Scripts\activate      #Windows
   
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   
4. Применяем миграции:
   ```bash
   alembic upgrade head
   
---
   
## Запуск

1. Запуск локально:
   ``` bash
   uvicorn main:app --reload

2. Запуск через Docker Compose
   ``` bash
   docker-compose up --build

---

## Примеры запросов

**Замечания:**
1. Значение x-token: "jfeoiajeofj"
2. При фильтрации задач через Postman параметр status должен иметь одно из следующих допустимых значений:
NEW, IN_PROGRESS, DONE. (Значения чувствительны к регистру и должны строго соответствовать перечислению StatusEnum, 
используемому в API.)
3. Формат даты: `YYYY-MM-DD`.\
   Пример: `2025-05-30`

**Примеры запросов (curl/Postman)**

***GET запрос получения задач по адресу 'http://127.0.0.1:8000/'***
1. Все задачи:
   ```bash
   curl --location --request GET 'http://127.0.0.1:8000/' \
   --header 'x-token: jfeoiajeofj' \
   --header 'Content-Type: application/json' \
   --data '
   '
2. C фильтрациями:
   ```bash
   curl --location --request GET 'http://127.0.0.1:8000?tasks_status=DONE&from_date=2025-05-15&to_date%20=2025-05-22' \
   --header 'x-token: jfeoiajeofj' \
   --header 'Content-Type: application/json' \
   --data '
   '
   
***GET запрос для получения задач по pk ('http://127.0.0.1:8000/task/{pk}/')***
   ```bash
   curl --location --request GET 'http://127.0.0.1:8000/task/1' \
   --header 'x-token: jfeoiajeofj' \
   --header 'Content-Type: application/json' \
   --data '
   '
```

***POST запрос для создания задач ('http://127.0.0.1:8000/create/')***
   ```bash
   curl --location 'http://127.0.0.1:8000/create' \
   --header 'x-token: jfeoiajeofj' \
   --header 'Content-Type: application/json' \
   --data '
   {
      "title": "Testing",
      "description": "testing the app",
      "due_date": "2025-05-22",
      "status": "in progress"
   }'
```

***PATCH запрос для обновления задач по pk ('http://127.0.0.1:8000/update/{pk}')***
   ```bash
   curl --location --request PATCH 'http://127.0.0.1:8000/update/2' \
   --header 'x-token: jfeoiajeofj' \
   --header 'Content-Type: application/json' \
   --data '
   {
      "status": "DONE"
   }'
```

***PATCH запрос для обновления задач по pk ('http://127.0.0.1:8000/update/{pk}')***
   ```bash
   curl --location --request DELETE 'http://127.0.0.1:8000/delete/2/' \
   --header 'x-token: jfeoiajeofj' \
   --header 'Content-Type: application/json' \
   --data '
   '
```

## Рефлексия

1. Что было самым сложным в задании?\
   Так как мой основной опыт связан с Django, реализация проекта на FastAPI потребовала изучения этого фреймворка. 
   Кроме того, мне пришлось настроить базу данных как для основного приложения, так и для тестовой среды.
   
2. Что получилось особенно хорошо?\
   Наиболее успешно, на мой взгляд, удалось реализовать функции для создания, чтения, обновления и 
   удаления данных (CRUD).

3. Что бы вы доработали при наличии времени?\
   На текущем этапе реализована простая авторизация, однако в будущем я бы добавила полноценную систему аутентификации 
   с использованием JWT.

4. Сколько времени заняло выполнение?\
   Весь проект был выполнен за 4 дня.

5. Чему вы научились при выполнении?\
   В процессе выполнения проекта я освоила основы работы с FastAPI, научилась настраивать базу данных, 
   использовать Alembic для миграций и реализовывать CRUD-функции с использованием SQLAlchemy.
