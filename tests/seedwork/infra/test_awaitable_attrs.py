import pytest
from sqlalchemy.exc import MissingGreenlet

from tests.seedwork.confdata.domain.entities import ExampleItem, Example
from tests.seedwork.confdata.domain.ports import ITestUnitOfWork


@pytest.mark.integration
async def test_orm_lazy_loading_with_awaitable_attrs_attributes(
    sql_uow: ITestUnitOfWork
) -> None:
    async with sql_uow as uow:
        new_example = Example(name="Example", items=[ExampleItem(name="item")])
        uow.examples.add(new_example)
        await uow.commit()

    async with sql_uow as uow:
        example = await uow.examples.get_by_id(new_example.id)
        with pytest.raises(MissingGreenlet):
            _ = example.items

        assert (await example.awaitable_attrs.items)[0].name == "item"
        example.items[0].name = "new item"
        example.items.append(ExampleItem(name="best item"))
        await uow.commit()

    async with sql_uow as uow:
        example = await uow.examples.get_by_id(new_example.id)
        with pytest.raises(MissingGreenlet):
            _ = example.items

        with pytest.raises(MissingGreenlet):
            _ = example.items

        await example.awaitable_attrs.items
        assert example.items[0].name == "new item"
        assert example.items[1].name == "best item"


@pytest.mark.unit
async def test_mem_lazy_loading_with_awaitable_attrs_attributes(
    mem_uow: ITestUnitOfWork,
) -> None:
    await test_orm_lazy_loading_with_awaitable_attrs_attributes(mem_uow)
