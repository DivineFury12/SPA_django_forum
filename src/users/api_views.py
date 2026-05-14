import datetime
import json
import http
import io

import django.http.multipartparser
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

import users.schemas
import forum.api_views


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


class ProfileController(dmr.Controller[dmr.plugins.pydantic.PydanticSerializer]):

    def _get_or_create_profile(self, user):
        profile, _ = users.models.Profile.objects.get_or_create(user=user)
        return profile

    def _parse_multipart(self):
        """Manually parse multipart data since Django skips it for PATCH."""
        body_file = io.BytesIO(self.request.body)
        parser    = django.http.multipartparser.MultiPartParser(
            self.request.META,
            body_file,
            self.request.upload_handlers,
            self.request.encoding,
        )
        post_data, file_data = parser.parse()
        return post_data, file_data

    @dmr.endpoint.modify(
        extra_responses=[
            dmr.metadata.ResponseSpec(return_type=dict, status_code=http.HTTPStatus.UNAUTHORIZED),
        ],
    )
    def get(self) -> users.schemas.ProfileSchema:
        user = forum.api_views.get_user_from_request(self.request)
        if user is None:
            raise dmr.response.APIError(
                {'detail': 'Authentication required.'},
                status_code=http.HTTPStatus.UNAUTHORIZED,
            )
        profile = self._get_or_create_profile(user)
        return users.schemas.ProfileSchema(
            username=user.username,
            nickname=profile.nickname or '',
            avatar=profile.avatar.url if profile.avatar else None,
        )

    @dmr.endpoint.modify(
        extra_responses=[
            dmr.metadata.ResponseSpec(return_type=dict, status_code=http.HTTPStatus.UNAUTHORIZED),
        ],
    )
    def patch(self) -> users.schemas.ProfileSchema:
        user = forum.api_views.get_user_from_request(self.request)
        if user is None:
            raise dmr.response.APIError(
                {'detail': 'Authentication required.'},
                status_code=http.HTTPStatus.UNAUTHORIZED,
            )

        profile = self._get_or_create_profile(user)

        content_type = self.request.content_type or ''
        if 'multipart' in content_type:
            post_data, file_data = self._parse_multipart()
            nickname = post_data.get('nickname', profile.nickname)
            avatar   = file_data.get('avatar')
            if avatar:
                profile.avatar = avatar
        else:
            body     = json.loads(self.request.body)
            nickname = body.get('nickname', profile.nickname)

        profile.nickname = nickname
        profile.save()

        print(f'Saved: nickname={profile.nickname}, avatar={profile.avatar}')

        return users.schemas.ProfileSchema(
            username=user.username,
            nickname=profile.nickname or '',
            avatar=profile.avatar.url if profile.avatar else None,
        )