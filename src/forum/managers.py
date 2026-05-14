from django.db import models
from django.utils import timezone


class PostsManager(models.Manager):

    def all_posts(self):
        return (
            self.select_related('author')
            .order_by('-created_at')
            .values(
                'id',
                'name',
                'description',
                'code',
                'created_at',
                'updated_at',
                author=models.F('author__username')
            )
        )

    def get_post(self, post_id):
        return (
            self.select_related('author')
            .filter(id=post_id)
            .values(
                'id',
                'name',
                'description',
                'code',
                'created_at',
                'updated_at',
                author=models.F('author__username')
            )
            .first()
        )

    def create_post(self, name, description, code, author_id):
        post = self.create(
            name=name,
            description=description,
            code=code,
            author_id=author_id,
        )
        return post.id

    def update_post(self, post_id, name=None, description=None, code=None):
        update_data = {}

        if name is not None:
            update_data['name'] = name

        if description is not None:
            update_data['description'] = description

        if code is not None:
            update_data['code'] = code

        if not update_data:
            return 0

        update_data['updated_at'] = timezone.now()

        return self.filter(id=post_id).update(**update_data)

    def delete_post(self, post_id):
        deleted_count, _ = self.filter(id=post_id).delete()
        return deleted_count