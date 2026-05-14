import datetime
import http

import dmr
import dmr.endpoint
import dmr.plugins.pydantic
import dmr.components
import dmr.response
import django.conf
import django.contrib.auth
import django.contrib.auth.models
import jwt
import pydantic


class LoginSchema(pydantic.BaseModel):
    username: str
    password: str


class RegisterSchema(pydantic.BaseModel):
    username: str
    password: str


class TokenSchema(pydantic.BaseModel):
    access: str
    refresh: str


def _create_tokens(user) -> TokenSchema:
    """Create JWT access and refresh tokens manually using pyjwt."""
    now = datetime.datetime.now(datetime.timezone.utc)
    secret = django.conf.settings.SECRET_KEY

    access_payload = {
        'user_id': user.id,
        'username': user.username,
        'is_staff': user.is_staff,
        'exp': now + datetime.timedelta(minutes=60),
        'type': 'access',
    }
    refresh_payload = {
        'user_id': user.id,
        'exp': now + datetime.timedelta(days=7),
        'type': 'refresh',
    }

    return TokenSchema(
        access=jwt.encode(access_payload, secret, algorithm='HS256'),
        refresh=jwt.encode(refresh_payload, secret, algorithm='HS256'),
    )


class LoginController(dmr.Controller[dmr.plugins.pydantic.PydanticSerializer]):
    
    @dmr.endpoint.modify(
        extra_responses=[
            dmr.metadata.ResponseSpec(
                return_type=dict,
                status_code=http.HTTPStatus.BAD_REQUEST,
            ),
            dmr.metadata.ResponseSpec(
                return_type=dict,
                status_code=http.HTTPStatus.UNAUTHORIZED,
            ),
        ],
    )
    def post(self, parsed_body: dmr.components.Body[LoginSchema]) -> TokenSchema:
        user = django.contrib.auth.authenticate(
            username=parsed_body.username,
            password=parsed_body.password,
        )
        if user is None:
            raise dmr.response.APIError(
                {'detail': 'Invalid credentials.'},
                status_code=http.HTTPStatus.UNAUTHORIZED,
            )
        return _create_tokens(user)


class RegisterController(dmr.Controller[dmr.plugins.pydantic.PydanticSerializer]):
    
    @dmr.endpoint.modify(
        extra_responses=[
            dmr.metadata.ResponseSpec(
                return_type=dict,
                status_code=http.HTTPStatus.BAD_REQUEST,
            ),
            dmr.metadata.ResponseSpec(
                return_type=dict,
                status_code=http.HTTPStatus.UNAUTHORIZED,
            ),
        ],
    )
    def post(self, parsed_body: dmr.components.Body[RegisterSchema]) -> TokenSchema:
        if django.contrib.auth.models.User.objects.filter(username=parsed_body.username).exists():
            raise dmr.response.APIError(
                {'detail': 'Пользователь уже существует.'},
                status_code=http.HTTPStatus.BAD_REQUEST,
            )

        user = django.contrib.auth.models.User.objects.create_user(
            username=parsed_body.username,
            password=parsed_body.password,
        )
        return _create_tokens(user)