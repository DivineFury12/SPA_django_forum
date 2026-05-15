import pydantic


class ProfileSchema(pydantic.BaseModel):
    username: str
    nickname: str
    avatar: str | None


class ProfileUpdateSchema(pydantic.BaseModel):
    nickname: str = ''


class LoginSchema(pydantic.BaseModel):
    username: str
    password: str


class RegisterSchema(pydantic.BaseModel):
    username: str
    password: str


class TokenSchema(pydantic.BaseModel):
    access: str
    refresh: str