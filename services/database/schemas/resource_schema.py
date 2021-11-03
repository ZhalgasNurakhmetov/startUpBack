from pydantic import BaseModel


class ResourceBaseSchema(BaseModel):
    from typing import Optional

    personal: bool
    available: bool
    title: bool
    author: bool
    year: Optional[str] = None
    pageCount: Optional[str] = None
    literature: str
    cover: Optional[str] = None
    language: str
    composition: str
    format: Optional[str] = None
    description: Optional[str] = None
    condition: Optional[str] = None


class ResourceCreateSchema(ResourceBaseSchema):
    ownerId: str


class ResourceSchema(ResourceBaseSchema):
    from typing import Any

    id: str
    ownerId: str
    owner: Any

    class Config:
        orm_mode = True
