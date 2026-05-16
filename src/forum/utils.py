import django.http
import jwt

import forum.models


def get_user_from_request(request):
    """Decode JWT from Authorization header and return the User."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(
            token,
            django.conf.settings.SECRET_KEY,
            algorithms=['HS256'],
        )
        return django.contrib.auth.models.User.objects.get(id=payload['user_id'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, django.contrib.auth.models.User.DoesNotExist):
        return None


class IsAuthorOrAdmin:
    """Reusable permission check."""
    @staticmethod
    def check(request: django.http.HttpRequest, post: forum.models.Posts) -> bool:
        return request.user.is_staff or post.author == request.user
