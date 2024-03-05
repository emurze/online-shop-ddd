from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from tests.utils.config import TestDatabaseConfig

db_config = TestDatabaseConfig()
db_dsn = db_config.get_dsn()
async_engine = create_async_engine(db_dsn, echo=True, poolclass=NullPool)
async_session_factory = async_sessionmaker(
    async_engine, expire_on_commit=False
)