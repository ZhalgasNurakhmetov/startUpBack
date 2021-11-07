from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    from datetime import datetime

    id: Optional[str] = None
    expires: Optional[datetime] = None


class UserCredentials(BaseModel):
    username: str
    password: str
