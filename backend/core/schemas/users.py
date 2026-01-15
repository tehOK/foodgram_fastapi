from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str

    model_config = ConfigDict(
        from_attributes=True,
    )

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )