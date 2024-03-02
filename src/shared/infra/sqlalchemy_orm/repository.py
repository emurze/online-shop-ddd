from typing import NoReturn, Any as Model

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from shared.domain.repository import IGenericRepository
from shared.infra.sqlalchemy_orm.ports import ICacheClient


class SqlAlchemyRepository(IGenericRepository):
    model: type[Model]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kw) -> Model:
        stmt = (
            insert(self.model)
            .values(**kw)
            .returning(self.model)
        )
        model = await self.session.execute(stmt)
        return model.scalar_one()

    async def get(self, **kw) -> Model:
        query = select(self.model).filter_by(**kw)
        res = await self.session.execute(query)
        model = res.scalars().first()
        return model

    async def list(self) -> NoReturn | list[Model]:
        query = select(self.model)
        posts = await self.session.execute(query)
        return list(posts.scalars().all())

    async def delete(self, **kw) -> Model:
        query = delete(self.model).filter_by(**kw).returning(self.model)
        model = await self.session.execute(query)
        return model.scalar_one()


class CachedSqlalchemyRepository(SqlAlchemyRepository):
    def __init__(self, session: AsyncSession, conn: ICacheClient) -> None:
        super().__init__(session)
        self.conn = conn

    async def get(self, **kw) -> Model:
        return await super().get(**kw)

    async def list(self) -> NoReturn | list[Model]:
        return await super().list()
