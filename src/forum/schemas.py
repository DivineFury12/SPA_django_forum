import datetime
import pydantic


class TagSchema(pydantic.BaseModel):
    id: int
    name: str


class PostSchema(pydantic.BaseModel):
    id: int
    name: str
    description: str
    code: str
    author: str
    tags: list[TagSchema]
    created_at: datetime.datetime


class PostCreateSchema(pydantic.BaseModel):
    name: str
    description: str
    tag_ids: list[int] = []