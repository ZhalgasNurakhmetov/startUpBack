from typing import List, Optional

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
    image: Optional[str] = None
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
    userId: str
    user: OwnerSchema

    class Config:
        orm_mode = True


class UserResourceSchema(UserResourceBaseSchema):

    favoriteUserList: List[UserLikedResourceSchema] = []

# TODO remove Optional before prod


class UserLikedResourceListSchema(BaseModel):
    id: str
    resourceId: Optional[str]
    resource: Optional[UserResourceSchema]

    class Config:
        orm_mode = True


class UserSchema(UserBaseSchema):

    id: str
    photo: Optional[str] = None
    about: Optional[str] = None
    resourceList: List[UserResourceSchema] = []
    favoriteResourceList: List[UserLikedResourceListSchema] = []
    following: List[OwnerSchema] = []
    followers: List[OwnerSchema] = []

    class Config:
        orm_mode = True


class UserEditSchema(BaseModel):
    firstName: str
    lastName: str
    birthDate: str
    city: str
    about: str
