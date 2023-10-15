import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from psycopg2.errors import UndefinedTable

from app.core.logger import logger
from tests.functional.config import postgres_config
from app.models.models import EmailTemlate, StoredEvent


@pytest.fixture()
def pg() -> Session:
    engine = create_engine(
        postgres_config.sqlalchemy_uri,
        future=postgres_config.future,
        echo=postgres_config.echo,
    )

    with Session(engine) as session:
        yield session


@pytest.fixture(autouse=True, scope='function')
def clear_pg(pg: Session) -> None:
    while True:
        try:
            pg.query(EmailTemlate).delete()
            pg.query(StoredEvent).delete()
            pg.commit()
            return
        except UndefinedTable as e:
            logger.error(e)


@pytest.fixture()
def init_pg(pg: Session) -> Session:
    pg.add(StoredEvent(
        name='test_event'
    ))
    pg.add(EmailTemlate(
        event_name='test_event',
        topic_message='test_topic',
        template='Hello, {{user.email}}!'
    ))
    pg.commit()
    yield pg
