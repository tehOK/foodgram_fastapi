from core.models import Ingredient

from . import BaseCRUD


class IngredientsCRUD(BaseCRUD):
    model = Ingredient