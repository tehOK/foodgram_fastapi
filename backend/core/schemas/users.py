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
    password: str | bytes

class UserRead(UserBase):
    id: int

class UserPasswordUpdate(BaseModel):
    new_password: str
    current_password: str

    model_config = ConfigDict(
        from_attributes=True,
    )

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )