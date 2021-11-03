from pydantic import BaseModel
from typing import List, Optional, Any


class UserBaseSchema(BaseModel):
    firstName: str
    lastName: str
    birthDate: str
    email: str
    city: str


class UserCreateSchema(UserBaseSchema):
    password: str


class UserSchema(UserBaseSchema):

    id: str
    photo: Optional[str] = None
    about: Optional[str] = None
    resourceList: List[Any] = []

    class Config:
        orm_mode = True
