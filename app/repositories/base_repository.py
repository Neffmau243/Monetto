from collections.abc import Mapping, Sequence
from typing import Any, Generic, TypeVar, cast

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    async def get(self, db: AsyncSession, object_id: int) -> ModelType | None:
        model = cast(Any, self.model)
        result = await db.execute(select(self.model).where(model.id == object_id))
        return result.scalars().first()

    async def list(
        self,
        db: AsyncSession,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType]:
        result = await db.execute(select(self.model).offset(offset).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, values: Mapping[str, Any]) -> ModelType:
        db_object = self.model(**values)
        db.add(db_object)
        await db.flush()
        await db.refresh(db_object)
        return db_object

    async def update(
        self, db: AsyncSession, db_object: ModelType, values: Mapping[str, Any]
    ) -> ModelType:
        for field, value in values.items():
            setattr(db_object, field, value)
        await db.flush()
        await db.refresh(db_object)
        return db_object

    async def delete(self, db: AsyncSession, db_object: ModelType) -> None:
        await db.delete(db_object)
        await db.flush()

    async def exists(self, db: AsyncSession, statement: Select[tuple[Any]]) -> bool:
        result = await db.execute(statement)
        return result.first() is not None
