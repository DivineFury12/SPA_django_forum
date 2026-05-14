import pydantic


class ProfileSchema(pydantic.BaseModel):
    username: str
    nickname: str
    avatar: str | None


class ProfileUpdateSchema(pydantic.BaseModel):
    nickname: str = ''