from auth.application.queries.get_clients import GetClientsQuery
from auth.application.query_handlers.get_clients import GetClientsHandler
from auth.domain.uow import IAuthUnitOfWork
from tests.unit.auth.conftest import make_client


async def test_get_clients_handler(uow: IAuthUnitOfWork) -> None:
    await make_client(uow, username="Vlad")
    await make_client(uow, username="Vlad")

    handler = GetClientsHandler(uow)
    query = GetClientsQuery()
    result = await handler.execute(query)
    clients = result.payload.clients

    assert len(clients) == 2