from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models.models import SqlalchemyBase

from app.core.config import postgres_config


engine = create_async_engine(
    postgres_config.sqlalchemy_uri,
    future=True,
    echo=True,
)


# create session for the interaction with database
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_pg_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SqlalchemyBase.metadata.drop_all)
        await conn.run_sync(SqlalchemyBase.metadata.create_all)
