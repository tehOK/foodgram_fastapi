from core.models import Tag

from . import BaseCRUD


class TagsCRUD(BaseCRUD):
    model = Tag