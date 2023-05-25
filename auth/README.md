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

1. Устанавливаем в .env POSTGRES_HOST и REDIS_HOST в значения localhost
2. Запускаем

        docker-compose -f docker-compose.dev.yaml up --build

3. Запускаем приложение

        flask --app app run

4. Остановка

        docker-compose -f docker-compose.dev.yaml down -v

5. Команда создания суперпользователя

        flask createsuperuser username password
