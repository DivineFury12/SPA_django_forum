import django.conf
import django.db.models

import forum.managers

class ForumBaseModel(django.db.models.Model):
    name = django.db.models.fields.TextField()
    created_at = django.db.models.fields.DateTimeField(auto_now_add=True)
    updated_at = django.db.models.fields.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Tags(ForumBaseModel):
    class Meta:
        default_related_name = 'tags'
    
    def __str__(self):
        return self.name


class Posts(ForumBaseModel):
    tags = django.db.models.ManyToManyField(Tags)
    author = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name='posts',
        related_query_name='posts',
    )
    description = django.db.models.fields.TextField()
    code = django.db.models.FileField(upload_to='forum/code/')
    
    objects = django.db.models.Manager()
    raw = forum.managers.PostsManager()
    
    
    