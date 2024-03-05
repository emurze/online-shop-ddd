import pytest
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import registry

from shared.domain.uow import IGenericUnitOfWork
from shared.infra.sqlalchemy_orm.common import suppress_echo
from shared.infra.sqlalchemy_orm import repository as r
from shared.infra.sqlalchemy_orm.uow import SqlAlchemyUnitOfWork
from tests.shared.conftest import (
    Example,
    IExampleRepository,
    IExampleUnitOfWork,
)

from tests.utils.db import async_session_factory, async_engine

mapped_registry = registry()

example_table = sa.Table(
    "example",
    mapped_registry.metadata,
    sa.Column("id", sa.BIGINT, primary_key=True),
    sa.Column("name", sa.String, nullable=False),
)

mapped_registry.map_imperatively(Example, example_table)


class ExampleSqlAlchemyRepository(r.SqlAlchemyRepository, IExampleRepository):
    model = Example


class ExampleSqlAlchemyUnitOfWork(SqlAlchemyUnitOfWork, IExampleUnitOfWork):
    pass


@pytest.fixture(scope="function", autouse=True)
async def restart_example_table():
    async with async_engine.begin() as conn:
        async with suppress_echo(async_engine):
            await conn.run_sync(mapped_registry.metadata.drop_all)
            await conn.run_sync(mapped_registry.metadata.create_all)
        await conn.commit()


@pytest.fixture
def repo(session: AsyncSession) -> IExampleRepository:
    return ExampleSqlAlchemyRepository(session)


@pytest.fixture
def uow() -> IGenericUnitOfWork:
    return ExampleSqlAlchemyUnitOfWork(
        session_factory=async_session_factory,
        examples=ExampleSqlAlchemyRepository,
    )