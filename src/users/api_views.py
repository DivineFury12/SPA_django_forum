import json
import http

import dmr
import dmr.endpoint
import dmr.plugins.pydantic
import dmr.components
import dmr.response
import django.conf
import django.contrib.auth
import django.contrib.auth.models

import users.schemas
import users.utils
import forum.utils


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
    def post(self, parsed_body: dmr.components.Body[users.schemas.LoginSchema]) -> users.schemas.TokenSchema:
        user = django.contrib.auth.authenticate(
            username=parsed_body.username,
            password=parsed_body.password,
        )
        if user is None:
            raise dmr.response.APIError(
                {'detail': 'Invalid credentials.'},
                status_code=http.HTTPStatus.UNAUTHORIZED,
            )
        return users.utils.create_tokens(user)


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
    def post(self, parsed_body: dmr.components.Body[users.schemas.RegisterSchema]) -> users.schemas.TokenSchema:
        if django.contrib.auth.models.User.objects.filter(username=parsed_body.username).exists():
            raise dmr.response.APIError(
                {'detail': 'Пользователь уже существует.'},
                status_code=http.HTTPStatus.BAD_REQUEST,
            )

        user = django.contrib.auth.models.User.objects.create_user(
            username=parsed_body.username,
            password=parsed_body.password,
        )
        return users.utils.create_tokens(user)


class ProfileController(dmr.Controller[dmr.plugins.pydantic.PydanticSerializer]):

    @dmr.endpoint.modify(
        extra_responses=[
            dmr.metadata.ResponseSpec(return_type=dict, status_code=http.HTTPStatus.UNAUTHORIZED),
        ],
    )
    def get(self) -> users.schemas.ProfileSchema:
        user = forum.utils.get_user_from_request(self.request)
        if user is None:
            raise dmr.response.APIError(
                {'detail': 'Authentication required.'},
                status_code=http.HTTPStatus.UNAUTHORIZED,
            )
        profile = users.utils.get_or_create_profile(user)
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
        user = forum.utils.get_user_from_request(self.request)
        if user is None:
            raise dmr.response.APIError(
                {'detail': 'Authentication required.'},
                status_code=http.HTTPStatus.UNAUTHORIZED,
            )

        profile = users.utils.get_or_create_profile(user)

        content_type = self.request.content_type or ''
        if 'multipart' in content_type:
            post_data, file_data = users.utils.parse_multipart()
            nickname = post_data.get('nickname', profile.nickname)
            avatar   = file_data.get('avatar')
            if avatar:
                profile.avatar = avatar
        else:
            body = json.loads(self.request.body)
            nickname = body.get('nickname', profile.nickname)

        profile.nickname = nickname
        profile.save()

        print(f'Saved: nickname={profile.nickname}, avatar={profile.avatar}')

        return users.schemas.ProfileSchema(
            username=user.username,
            nickname=profile.nickname or '',
            avatar=profile.avatar.url if profile.avatar else None,
        )