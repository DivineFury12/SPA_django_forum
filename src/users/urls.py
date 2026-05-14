import django.contrib.auth.views
import django.urls
import users.views
import users.api_views

app_name = 'users'

urlpatterns = [
    django.urls.path(
        'login/',
        django.contrib.auth.views.LoginView.as_view(template_name='users/login.html'),
        name='login',
    ),
    django.urls.path(
        'logout/',
        django.contrib.auth.views.LogoutView.as_view(),
        name='logout',
    ),
    django.urls.path('auth/register/', users.api_views.RegisterController.as_view(), name='api_register'),
]