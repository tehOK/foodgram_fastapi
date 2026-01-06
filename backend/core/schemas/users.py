from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    username: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True,
    )

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int