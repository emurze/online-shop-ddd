import uuid

from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, MappedColumn, Mapped

from seedwork.domain.mappers import IDataMapper
from seedwork.domain.repositories import IGenericRepository
from seedwork.infra.database import ModelBase
from seedwork.infra.repository import SqlAlchemyRepository
from tests.seedwork.confdata.domain import Example


class Model(ModelBase, AsyncAttrs, DeclarativeBase):
    __allow_unmapped__ = True
    id: Mapped[uuid.UUID]


class ExampleModel(Model):
    __tablename__ = "example"
    id = MappedColumn(UUID, primary_key=True)
    name = Column(String(Example.c.name.max_length), nullable=False)


# class ExampleItemModel(Model):
#     id = MappedColumn(UUID, primary_key=True)
#     name = Column(String, nullable=False)
#     example_id = Column(String, ForeignKey("example.id"), nullable=False)
#
#
# class AddressModel(Model):
#     id = MappedColumn(UUID, primary_key=True)
#     city = Column(String, nullable=False)
#     example_item_id = Column(
#         String, ForeignKey("example_item.id"), nullable=False
#     )


class ExampleMapper(IDataMapper):
    def entity_to_model(self, entity: Example) -> ExampleModel:
        return ExampleModel(**entity.model_dump())

    def model_to_entity(self, model: ExampleModel) -> Example:
        return Example.model_validate(model)


class ExampleSqlAlchemyRepository(SqlAlchemyRepository, IGenericRepository):
    mapper_class = ExampleMapper
    model_class = ExampleModel
