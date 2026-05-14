from app.dto.category_dto import CategoryOut
from app.models.category import Category


def category_to_out(category: Category) -> CategoryOut:
    dto = CategoryOut.model_validate(category)
    dto.display_order = category.sort_order
    return dto
