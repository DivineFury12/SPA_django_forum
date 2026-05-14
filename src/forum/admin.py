import django.contrib.admin
import forum.models


@django.contrib.admin.register(forum.models.Tags)
class TagsAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


@django.contrib.admin.register(forum.models.Posts)
class PostsAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('name', 'author', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'author__username')
    list_filter = ('tags', 'created_at')
    filter_horizontal = ('tags',)  # nicer widget for ManyToMany
    readonly_fields = ('created_at', 'updated_at')