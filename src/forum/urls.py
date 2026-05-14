import django.urls
import forum.api_views

urlpatterns = [
    django.urls.path('posts/', forum.api_views.PostListController.as_view(),   name='post_list'),
    django.urls.path('posts/<int:post_id>/', forum.api_views.PostDetailController.as_view(), name='post_detail'),
]