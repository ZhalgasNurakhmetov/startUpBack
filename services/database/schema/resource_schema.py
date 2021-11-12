

from pydantic import BaseModel
from typing import Optional


class ResourceBaseSchema(BaseModel):

    personal: bool
    title: str
    author: str
    year: Optional[str] = None
    pageCount: Optional[str] = None
    literature: str
    cover: Optional[str] = None
    language: str
    composition: str
    format: Optional[str] = None
    description: Optional[str] = None
    condition: Optional[str] = None


class OwnerSchema(BaseModel):
    id: str
    photo: Optional[str] = None
    about: Optional[str] = None
    firstName: str
    lastName: str
    birthDate: str
    username: str
    city: str

    class Config:
        orm_mode = True


class ResourceSchema(ResourceBaseSchema):
    from typing import List

    id: str
    available: bool
    likes: int
    ownerId: str
    owner: OwnerSchema
    # likedUserList: List[OwnerSchema] = []

    class Config:
        orm_mode = True
