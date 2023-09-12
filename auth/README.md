# Микросервис авторизации

1. Flask.
2. SQLAlchemy в качестве ORM.
3. Marshmallow для валидации и сериализации.
4. Храним Json Web Tokens в Redis.
6. Ролевая модель разграничения доступов.

## How to Use

1. Запускам docker-compose

        docker-compose up --build

2. Остановка:

        docker-compose down -v

3. Сервис будет доступен по адресу http://localhost:8100, для авторизации используется сервисный токен

4. Документация OpenAPI: [http://localhost:5000/swagger/doc](http://localhost:5000/swagger/doc)

## Разработка (инструкция для Visual Studio Code)

1. В целях удобства разработки используем облегченный [DNS сервер](https://hub.docker.com/r/defreitas/dns-proxy-server). Это позволит получать доступ к любому контейнеру по установленному параметру hostname из docker-compose без какого-либо выставления портов. Запустим DNS сервер командой:

        docker run --rm --hostname dns.mageddo \
        --name dns.mageddo \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v /etc/resolv.conf:/etc/resolv.conf \
        defreitas/dns-proxy-server

2. Если в VS Code не установлено расширение Dev Containers, необходимо его установить. Расширение используется для удобства разработки внутри контейнера, запущенного из docker-compose, кроме того, для унификации окружения разработки внутри команды.

3. Запустив VS Code из директории с микросервисом (папка auth), редактор определит настройки контейнера разработки (.devcontainer.json). Далее из палитры команд (Ctrl+Shift+P) вызываем "Dev Containers: Rebuild and Reopen in Container". VS Code поднимет docker-compose файл, примонтирует корневую директорию в соответствующий контейнер и перезапустится внутри него.

4. Внутри контейнера применяем миграции

        flask db upgrade

5. Загружаем данные для отладки

        flask load_debug_data

   теперь можно использовать сервисный токен

6. Запускаем приложение

        flask --app app run --debug --host 0.0.0.0 --port 8000

7. Для остановки контейнеров, запущеных из docker-compose, выбираем "Dev Containers: Reopen Foldier Locally"

8. Останавливаем DNS сервер

        docker stop dns.mageddo
