from . import BaseCRUD
from core.models import Ingredient

class IngredientsCRUD(BaseCRUD):
    model = Ingredient