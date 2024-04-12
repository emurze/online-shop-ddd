import pytest

from seedwork.infra.database import suppress_echo
from tests.conftest import engine
from tests.seedwork.confdata.repositories import Model


@pytest.fixture(scope="function")
async def _restart_example_table() -> None:
    async with engine.begin() as conn:
        async with suppress_echo(engine):
            await conn.run_sync(Model.metadata.drop_all)
            await conn.run_sync(Model.metadata.create_all)
        await conn.commit()
