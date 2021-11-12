from typing import List, Optional, Any

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    firstName: str
    lastName: str
    birthDate: str
    username: str
    city: str


class OwnerSchema(UserBaseSchema):
    id: str
    photo: Optional[str] = None
    about: Optional[str] = None

    class Config:
        orm_mode = True


class UserResourceBaseSchema(BaseModel):
    id: str
    available: bool
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
    likes: int
    ownerId: str
    owner: OwnerSchema

    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
    password: str


class UserLikedResourceSchema(BaseModel):
    id: str
    user_id: str
    user: OwnerSchema

    class Config:
        orm_mode = True


class UserLikedResourceListSchema(BaseModel):
    id: str
    resource_id: str
    resource: UserResourceBaseSchema

    class Config:
        orm_mode = True


class UserResourceSchema(UserResourceBaseSchema):

    likedUserList: List[UserLikedResourceSchema] = []


class UserSchema(UserBaseSchema):

    id: str
    photo: Optional[str] = None
    about: Optional[str] = None
    resourceList: List[UserResourceSchema] = []
    likedResourceList: List[UserLikedResourceListSchema] = []

    class Config:
        orm_mode = True


class UserEditSchema(BaseModel):
    firstName: str
    lastName: str
    birthDate: str
    city: str
    about: str
