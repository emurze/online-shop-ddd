import abc

from shared.application.dtos import Model, OutputDto


class Query(Model):
    pass


class IQueryHandler(abc.ABC):
    @abc.abstractmethod
    async def handle(self, query: Query) -> OutputDto: ...
