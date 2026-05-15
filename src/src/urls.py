import django.contrib.admin
import django.conf
import django.conf.urls.static
import django.urls
import dmr.routing

import docs.urls
import homepage.urls
import forum.urls
import users.urls
import users.api_views

# dmr API router
router = dmr.routing.Router(
    'api/',
    [
        django.urls.path('', django.urls.include(docs.urls)),
        django.urls.path('auth/login/', users.api_views.LoginController.as_view(), name='api-login'),
        django.urls.path('auth/register/', users.api_views.RegisterController.as_view(), name='api-register'),
        django.urls.path('users/',   django.urls.include(users.urls)),

    ],
)

urlpatterns = [
    django.urls.path('admin/',   django.contrib.admin.site.urls),
    django.urls.path('',         django.urls.include(homepage.urls)),
    django.urls.path('forum/',   django.urls.include(forum.urls)),

    django.urls.path(router.prefix, django.urls.include((router.urls, 'api'), namespace='api')),

] + django.conf.urls.static.static(
    django.conf.settings.MEDIA_URL,
    document_root=django.conf.settings.MEDIA_ROOT,
)