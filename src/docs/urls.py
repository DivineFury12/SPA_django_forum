import django.urls

import forum.api_views

app_name = 'docs'

urlpatterns = [
    django.urls.path('posts/', forum.api_views.PostListController.as_view(),   name='post_list'),
    django.urls.path('posts/<int:post_id>/', forum.api_views.PostDetailController.as_view(), name='post_detail'),
    django.urls.path('tags/', forum.api_views.TagListController.as_view(), name='tag_list'),
]