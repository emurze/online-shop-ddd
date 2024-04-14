import pytest

from tests.seedwork.confdata.domain import Example
from tests.seedwork.confdata.ports import ITestUnitOfWork


class TestMemoryUoW:
    @pytest.mark.unit
    async def test_uow_can_commit(self, mem_uow: ITestUnitOfWork) -> None:
        async with mem_uow as uow:
            example = Example(name="Hello")
            await uow.examples.add(example)
            await uow.commit()

        async with mem_uow as uow:
            example = await uow.examples.get_by_id(example.id)
            assert example.name == "Hello"

    @pytest.mark.unit
    async def test_uow_can_rollback(self, mem_uow: ITestUnitOfWork) -> None:
        async with mem_uow as uow:
            example = Example(name="Hello")
            await uow.examples.add(example)
            await uow.rollback()

        async with mem_uow as uow:
            example = await uow.examples.get_by_id(example.id)
            assert example is None

    @pytest.mark.unit
    async def test_uow_can_do_commit_rollback_pipeline(
        self, mem_uow: ITestUnitOfWork
    ) -> None:
        async with mem_uow as uow:
            await uow.examples.add(Example(name="Hello 1"))
            await uow.commit()

        async with mem_uow as uow:
            await uow.examples.add(Example(name="Hello 2"))
            await uow.examples.add(Example(name="Hello 3"))
            await uow.commit()

        async with mem_uow as uow:
            await uow.examples.add(Example(name="Hello"))

        async with mem_uow as uow:
            await uow.examples.add(Example(name="Hello"))
            await uow.rollback()

        async with mem_uow as uow:
            await uow.examples.add(Example(name="Hello 4"))
            await uow.commit()

        async with mem_uow as uow:
            assert await uow.examples.count() == 4


class TestSqlAlchemyUoW:
    mem_tests = TestMemoryUoW()

    @pytest.mark.integration
    async def test_uow_can_commit(self, sql_uow: ITestUnitOfWork) -> None:
        await self.mem_tests.test_uow_can_commit(sql_uow)

    @pytest.mark.integration
    async def test_uow_can_rollback(self, sql_uow: ITestUnitOfWork) -> None:
        await self.mem_tests.test_uow_can_rollback(sql_uow)

    @pytest.mark.integration
    async def test_uow_can_do_commit_rollback_pipeline(
        self, sql_uow: ITestUnitOfWork
    ) -> None:
        await self.mem_tests.test_uow_can_do_commit_rollback_pipeline(sql_uow)
