from typing import Optional

from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    from datetime import datetime

    id: Optional[str] = None
    expires: Optional[datetime] = None


class UserCredentialsSchema(BaseModel):
    username: str
    password: str
