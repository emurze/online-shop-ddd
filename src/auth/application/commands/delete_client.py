from dataclasses import dataclass

from auth.application.commands.create_client import CreateClientCommand
from auth.domain.uow import IAuthUnitOfWork
from shared.application.command_handler import ICommandHandler
from shared.application.commands import CommandResult


class DeleteClientCommand(CreateClientCommand):
    id: int


@dataclass(frozen=True, slots=True)
class DeleteClientCommandHandler(ICommandHandler):
    uow: IAuthUnitOfWork

    async def execute(self, command: DeleteClientCommand) -> CommandResult:
        try:
            async with self.uow:
                await self.uow.clients.delete(id=command.id)
                await self.uow.commit()
                return CommandResult()
        except SystemError:
            return CommandResult.build_system_error()
