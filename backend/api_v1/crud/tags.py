from . import BaseCRUD
from core.models import Tag

class TagsCRUD(BaseCRUD):
    model = Tag