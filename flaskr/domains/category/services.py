from typing import Any, Dict

from flaskr.core.base.services import BaseService
from flaskr.domains.category.models import Category
from flaskr.domains.category.repositories import CategoryRepository


class CategoryService(BaseService):
    repository = CategoryRepository()

    def create_new_category(self, data: Dict[str, Any]) -> Dict | None:
        return self.create_new_item(
            model_class=Category,
            unique_key=data["name"],
            column_name="name",
            **data,
        )
