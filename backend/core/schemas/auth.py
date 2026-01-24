from pydantic import BaseModel


class TokenInfo(BaseModel):
    auth_token: str