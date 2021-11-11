from typing import Any
from typing import Optional

from pydantic import BaseModel


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


class ResourceSchema(ResourceBaseSchema):

    id: str
    available: bool
    ownerId: str
    owner: Any

    class Config:
        orm_mode = True
