import http
import json

import dmr
import dmr.endpoint
import dmr.plugins.pydantic
import dmr.components
import django.shortcuts


import forum.models
import forum.schemas
import forum.utils



class TagListController(dmr.Controller[dmr.plugins.pydantic.PydanticSerializer]):
    def get(self) -> list[forum.schemas.TagSchema]:
        tags = forum.models.Tags.objects.all().order_by('name')
        return [forum.schemas.TagSchema(id=t.id, name=t.name) for t in tags]


class PostListController(dmr.Controller[dmr.plugins.pydantic.PydanticSerializer]):

    def get(self) -> list[forum.schemas.PostSchema]:
        """List all posts."""
        posts = forum.models.Posts.objects.all_posts()
        return [
            forum.schemas.PostSchema(
                id=p.id,
                name=p.name,
                description=p.description,
                code=p.code.url if p.code else '',
                author=p.author.username,
                tags=[forum.schemas.TagSchema(id=t.id, name=t.name) for t in p.tags.all()],
                created_at=p.created_at,
                author_nickname=p.author.profile.nickname,
                author_avatar=p.author.profile.avatar.url if p.author.profile.avatar else None,
            )
            for p in posts
        ]

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
    def post(self) -> forum.schemas.PostSchema:
        user = forum.utils.get_user_from_request(self.request)
        if user is None:
            raise dmr.response.APIError(
                {'detail': 'Authentication required.'},
                status_code=http.HTTPStatus.UNAUTHORIZED,
            )
        # https://docs.djangoproject.com/en/6.0/ref/request-response
        name = self.request.POST.get('name')
        description = self.request.POST.get('description')
        code_file = self.request.FILES.get('code')

        if not name or not description:
            raise dmr.response.APIError(
                {'detail': 'name and description are required.'},
                status_code=http.HTTPStatus.BAD_REQUEST,
            )

        post = forum.models.Posts.objects.create(
            name=name,
            description=description,
            author=user,
            code=code_file,
        )

        tag_ids = self.request.POST.getlist('tag_ids')
        if tag_ids:
            post.tags.set(tag_ids)

        return forum.schemas.PostSchema(
            id=post.id,
            name=post.name,
            description=post.description,
            code=post.code.url if post.code else '',
            author=post.author.username,
            tags=[forum.schemas.TagSchema(id=t.id, name=t.name) for t in post.tags.all()],
            created_at=post.created_at,
            author_nickname=post.author.profile.nickname,
            author_avatar=post.author.profile.avatar.url if post.author.profile.avatar else None,
        )


class PostDetailController(dmr.Controller[dmr.plugins.pydantic.PydanticSerializer]):

    @dmr.endpoint.modify(
    extra_responses=[
        dmr.metadata.ResponseSpec(return_type=dict, status_code=http.HTTPStatus.NOT_FOUND),
    ],
)
    def get(self) -> forum.schemas.PostSchema:
        post_id = self.kwargs.get('post_id')
        post = django.shortcuts.get_object_or_404(
            forum.models.Posts.objects.select_related('author').prefetch_related('tags'),
            id=post_id,
        )
        return forum.schemas.PostSchema(
            id=post.id,
            name=post.name,
            description=post.description,
            code=post.code.url if post.code else '',
            author=post.author.username,
            tags=[forum.schemas.TagSchema(id=t.id, name=t.name) for t in post.tags.all()],
            created_at=post.created_at,
            author_nickname=post.author.profile.nickname,
            author_avatar=post.author.profile.avatar.url if post.author.profile.avatar else None,
        )

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
    def patch(self) -> forum.schemas.PostSchema:
        post_id = self.kwargs.get('post_id')

        user = forum.utils.get_user_from_request(self.request)
        if user is None:
            raise dmr.response.APIError(
                {'detail': 'Authentication required.'},
                status_code=http.HTTPStatus.UNAUTHORIZED,
            )

        post = django.shortcuts.get_object_or_404(forum.models.Posts, id=post_id)

        if not (user.username == post.author.username or user.is_staff):
            raise dmr.response.APIError(
                {'detail': 'Permission denied.'},
                status_code=http.HTTPStatus.FORBIDDEN,
            )

        body = json.loads(self.request.body)
        name = body.get('name')
        description = body.get('description')

        if name:
            post.name = name
        if description:
            post.description = description
        post.save()

        return forum.schemas.PostSchema(
            id=post.id,
            name=post.name,
            description=post.description,
            code=post.code.url if post.code else '',
            author=post.author.username,
            tags=[forum.schemas.TagSchema(id=t.id, name=t.name) for t in post.tags.all()],
            created_at=post.created_at,
            author_nickname=post.author.profile.nickname,
            author_avatar=post.author.profile.avatar.url if post.author.profile.avatar else None,
        )
        
    def delete(self) -> None:
        post_id = self.kwargs.get('post_id')

        user = forum.utils.get_user_from_request(self.request)
        if user is None:
            raise dmr.response.APIError(
                {'detail': 'Authentication required.'},
                status_code=http.HTTPStatus.UNAUTHORIZED,
            )

        post = django.shortcuts.get_object_or_404(forum.models.Posts, id=post_id)

        if not (user.username == post.author.username or user.is_staff):
            raise dmr.response.APIError(
                {'detail': 'Permission denied.'},
                status_code=http.HTTPStatus.FORBIDDEN,
            )

        post.delete()