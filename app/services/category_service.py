from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.category_dto import CategoryCreate, CategoryOut, CategoryUpdate
from app.exceptions.domain import ConflictError, ForbiddenError, NotFoundError
from app.mappers.category_mapper import category_to_out
from app.models.category import Category
from app.models.enums import TransactionType
from app.repositories.category_repository import CategoryRepository, category_repository


class CategoryService:
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    async def list_categories(
        self,
        db: AsyncSession,
        user_id: int,
        category_type: TransactionType | None = None,
    ) -> list[CategoryOut]:
        categories = await self.repository.list_for_user(db, user_id, category_type)
        category_dtos = [category_to_out(category) for category in categories]
        for index, category in enumerate(category_dtos, start=1):
            category.display_order = index
        return category_dtos

    async def create_category(
        self, db: AsyncSession, user_id: int, category_in: CategoryCreate
    ) -> CategoryOut:
        await self._ensure_unique(
            db, user_id=user_id, name=category_in.name, category_type=category_in.type
        )
        category = await self.repository.create(
            db,
            {
                "name": category_in.name,
                "type": category_in.type,
                "user_id": user_id,
                "is_default": False,
                "sort_order": 1000,
            },
        )
        return category_to_out(category)

    async def update_category(
        self, db: AsyncSession, user_id: int, category_id: int, category_in: CategoryUpdate
    ) -> CategoryOut:
        category = await self._get_editable_category(db, user_id, category_id)
        values = category_in.model_dump(exclude_unset=True)
        target_name = values.get("name", category.name)
        target_type = values.get("type", category.type)
        if "type" in values and target_type != category.type:
            await self._ensure_type_can_change(db, category)
        await self._ensure_unique(
            db,
            user_id=user_id,
            name=target_name,
            category_type=target_type,
            exclude_id=category.id,
        )
        updated = await self.repository.update(db, category, values)
        return category_to_out(updated)

    async def delete_category(self, db: AsyncSession, user_id: int, category_id: int) -> None:
        category = await self._get_editable_category(db, user_id, category_id)
        transaction_count = await self.repository.count_transactions(db, category.id)
        if transaction_count:
            raise ConflictError("Category has associated transactions")
        await self.repository.delete(db, category)

    async def _get_editable_category(
        self, db: AsyncSession, user_id: int, category_id: int
    ) -> Category:
        category = await self.repository.get(db, category_id)
        if not category:
            raise NotFoundError("Category not found")
        if category.user_id != user_id:
            raise ForbiddenError("You can only modify your own categories")
        return category

    async def _ensure_type_can_change(self, db: AsyncSession, category: Category) -> None:
        transaction_count = await self.repository.count_transactions(db, category.id)
        if transaction_count:
            raise ConflictError("Category has associated transactions")

    async def _ensure_unique(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        name: str,
        category_type,
        exclude_id: int | None = None,
    ) -> None:
        duplicate = await self.repository.get_duplicate(
            db,
            user_id=user_id,
            name=name,
            category_type=category_type,
            exclude_id=exclude_id,
        )
        if duplicate:
            raise ConflictError("Category name already exists for this type")


category_service = CategoryService(category_repository)
