from typing import Any, Callable

from dependency_injector import containers
from dependency_injector.providers import Factory, Singleton

from seedwork.infra.injector import Link
from seedwork.infra.repository import InMemoryRepository
from seedwork.infra.uows import InMemoryUnitOfWork, SqlAlchemyUnitOfWork
from seedwork.presentation.factories import get_dict, get_bus, get_handler
from tests.conftest import session_factory
from tests.seedwork.confdata.handlers.command import create_example
from tests.seedwork.confdata.repositories import ExampleSqlAlchemyRepository


class SqlAlchemySeedWorkContainer(containers.DeclarativeContainer):
    db_session_factory = Link(session_factory)
    uow_factory: Any = Singleton(
        Factory,
        SqlAlchemyUnitOfWork,
        session_factory=db_session_factory,
        examples=ExampleSqlAlchemyRepository,
    )

    query_handlers: Callable = Singleton(get_dict)
    command_handlers: Callable = Singleton(
        get_dict,
        Singleton(get_handler, create_example, uow=uow_factory),
    )
    event_handlers: Callable = Singleton(get_dict)
    message_bus: Callable = Singleton(
        get_bus,
        query_handlers=query_handlers,
        command_handlers=command_handlers,
        event_handlers=event_handlers,
    )


def get_memory_container():
    container = SqlAlchemySeedWorkContainer()
    container.uow_factory.override(
        Singleton(
            Factory,
            InMemoryUnitOfWork,
            examples=InMemoryRepository,
        )
    )
    return container


sql_container = SqlAlchemySeedWorkContainer()
