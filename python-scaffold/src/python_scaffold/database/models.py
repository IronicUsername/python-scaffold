"""Module to structure the db data."""
from dataclasses import dataclass, field
from typing import Any, Final
from uuid import UUID, uuid4

from sqlalchemy import MetaData
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.orm import DeclarativeMeta, registry
from sqlalchemy.schema import Column

from .. import settings

metadata_obj = MetaData(schema=settings.database_schema_name)
mapper_registry: Final[registry] = registry(metadata=metadata_obj)


class Base(metaclass=DeclarativeMeta):
    """Base to initialize the database models."""

    __abstract__ = True

    registry = mapper_registry
    metadata = mapper_registry.metadata

    __init__ = mapper_registry.constructor


@dataclass
class HasMetadataKey:
    """Set metadata_key in child objects."""

    __sa_dataclass_metadata_key__ = "sa"

    def __post_init__(self, *args: Any) -> None:
        """Call after init.

        Use to add table relationships or other functionality after the initialization of the table.
        Example case: We want to connect `Table1` and `Table2` to have an
        optional relation from `Table1` to `Table2`'s `id` field.

        Example on usage:

        class Table(HasMetadataKey):
            id: UUID = field(...)
            table_2_id: UUID = field(...)  # has nullable relation to Table2's `id` field.

            table_2: Optional[Table2] = field(default=None, init=False)

            def __post_init__(self, *args: Any) -> None:
                super().__post_init__(*args)
                if self.table_2"
                    self.table_2_id = self.table_2.id
        """


@mapper_registry.mapped
@dataclass
class ExampleTable(HasMetadataKey):
    """Table storing triggered endpoint history."""

    __tablename__ = "example_table"
    id: UUID = field(  # noqa: VNE003
        init=False, metadata={"sa": Column("id", psql.UUID(as_uuid=True), primary_key=True)}, default_factory=uuid4
    )
    text: str = field(metadata={"sa": Column("text", psql.TEXT)})
