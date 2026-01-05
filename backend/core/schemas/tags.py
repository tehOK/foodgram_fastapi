from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    id: int
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)

class TagRead(TagBase):
    pass