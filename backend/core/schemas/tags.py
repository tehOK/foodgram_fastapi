from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class TagBase(BaseModel):
    id: int
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)

class TagRead(TagBase):
    pass

class TagInRecipe(TagBase):
    pass

class TagForRecipe(BaseModel):
    id: int