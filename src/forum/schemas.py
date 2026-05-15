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
    author_nickname: str
    author_avatar: str | None
    tags: list[TagSchema]
    created_at: datetime.datetime


class PostCreateSchema(pydantic.BaseModel):
    name: str
    description: str
    tag_ids: list[int] = []