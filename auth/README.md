# Микросервис авторизации

Название говорит само за себя, это не просто сервис авторизации, а особенный микросервис с интересными фичами:

1. Flask (gevent).
2. SQLAlchemy в качестве ORM.
3. Marshmallow для валидации/сериализации.
4. Регистрация пользователей, basic и JWT авторизация.
5. Ролевая модель разграничения доступов.


## Запуск

1. Переименовать демонстрационнный .env.example в .env
2. Выполнить

        docker-compose -f docker-compose.prod.yaml up --build

3. Остановка:

        docker-compose -f docker-compose.dev.yaml down -v

4. Документация OpenAPI: [http://localhost:5000/swagger/](http://localhost:5000/swagger/)

## Разработка

1. Установить в .env значения для POSTGRES_HOST, REDIS_HOST, API_HOST = localhost
2. Запустить окружение

        docker-compose -f docker-compose.dev.yaml up --build

3. Применить миграции

        flask db upgrade

4. Создать суперпользователя

        flask createsuperuser username password

5. Запустить приложение

        flask --app app run

6. Остановка

        docker-compose -f docker-compose.dev.yaml down -v


# Тестирование

1. Для запуска функциональных тестов запустить

        docker-compose -f tests/functional/docker-compose.yaml  up --build

2. Для отладки тестов запустить окружение для разработки (см. пункт разработка).

3. Далее выполняем

        pytest
