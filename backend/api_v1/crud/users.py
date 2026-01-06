from api_v1.crud import BaseCRUD
from core.models import User

class UsersCRUD(BaseCRUD):
    model = User