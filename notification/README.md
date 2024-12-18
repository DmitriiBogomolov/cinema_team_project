Для разработки:

1. запустить днс
```dockerfile
docker run --rm --hostname dns.mageddo --name dns.mageddo -v /var/run/docker.sock:/var/run/docker.sock -v /etc/resolv.conf:/etc/resolv.conf defreitas/dns-proxy-server
```

3. запустить приложение
```python
docker-compose up --build
```

можно запускать локально:
```python
uvicorn app.main:app --reload
```


далее дергаем ручку 127.0.0.1:8000/api/v1/events передавая туда
{
    "initiating_service_name": "auth_service",
    "initiating_user_id": "6b7aae84-517d-11ee-be56-0242ac120002",
    "description": "some_description",
    "event_name": "review_comment_received",
    "priority": 0,
    "user_ids": ["6b7aae84-517d-11ee-be56-0242ac120002"]
}

для (ручная рассылка): 127.0.0.1:8000/api/v1/events/send_manual
{
    "initiating_service_name": "auth_service",
    "initiating_user_id": "6b7aae84-517d-11ee-be56-0242ac120002",
    "description": "some_description",
    "event_name": "review_comment_received",
    "priority": 0,
    "user_ids": ["6b7aae84-517d-11ee-be56-0242ac120002"],
    "topic_message": "hello",
    "email": "Hello {{user.email}}"
}

----------------------------------

Для накатывания миграций, если файла alembic.ini ещё нет, нужно запустить в терминале команду:

alembic init migrations
После этого будет создана папка с миграциями и конфигурационный файл для алембика.


В alembic.ini нужно задать адрес базы данных, в которую будем катать миграции.
Дальше идём в папку с миграциями и открываем env.py, там вносим изменения в блок, где написано
from myapp import mymodel
(указать базовую модель алхимии
from app.models.models import SqlalchemyBase
target_metadata = SqlalchemyBase.metadata)
Дальше вводим: alembic revision --autogenerate -m "comment"
Будет создана миграция

Накатываем миграции: alembic upgrade heads
