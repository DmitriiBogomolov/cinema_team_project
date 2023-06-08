# Микросервис авторизации

1. Flask.
2. SQLAlchemy в качестве ORM.
3. Marshmallow для валидации и сериализации.
4. Храним Json Web Tokens в Redis.
6. Ролевая модель разграничения доступов.

## Запуск

1. Переименовать демонстрационнный .env.example в .env
2. Выполнить

        docker-compose -f docker-compose.prod.yaml up --build

3. Остановка:

        docker-compose -f docker-compose.dev.yaml down -v

4. Документация OpenAPI: [http://localhost:5000/swagger/doc](http://localhost:5000/swagger/doc)

## Разработка

1. Установить в .env значения для POSTGRES_HOST, REDIS_HOST, API_HOST = localhost
2. Запустить окружение

        docker-compose -f docker-compose.dev.yaml up --build

3. Применить миграции

        flask db upgrade

4. Создать суперпользователя

        flask createsuperuser superuser@inbox.com supassword

5. Запустить приложение

        flask --app app run --debug

6. Остановка

        docker-compose -f docker-compose.dev.yaml down -v


# Тестирование

1. Для запуска функциональных тестов запустить

        docker-compose -f tests/functional/docker-compose.yaml  up --build

2. Для отладки тестов запустить окружение для разработки (см. пункт разработка).

3. Далее выполняем

        pytest
