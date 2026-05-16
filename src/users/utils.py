import datetime
import io

import django.http
import jwt

import users.models

def get_or_create_profile(user):
    profile, _ = users.models.Profile.objects.get_or_create(user=user)
    return profile

def parse_multipart(self):
    """Manually parse multipart data since Django skips it for PATCH."""
    body_file = io.BytesIO(self.request.body)
    parser    = django.http.multipartparser.MultiPartParser(
        self.request.META,
        body_file,
        self.request.upload_handlers,
        self.request.encoding,
    )
    post_data, file_data = parser.parse()
    return post_data, file_data

def create_tokens(user) -> users.schemas.TokenSchema:
    """Create JWT access and refresh tokens manually using pyjwt."""
    now = datetime.datetime.now(datetime.timezone.utc)
    secret = django.conf.settings.SECRET_KEY

    access_payload = {
        'user_id': user.id,
        'username': user.username,
        'is_staff': user.is_staff,
        'exp': now + datetime.timedelta(minutes=60),
        'type': 'access',
    }
    refresh_payload = {
        'user_id': user.id,
        'exp': now + datetime.timedelta(days=7),
        'type': 'refresh',
    }

    return users.schemas.TokenSchema(
        access=jwt.encode(access_payload, secret, algorithm='HS256'),
        refresh=jwt.encode(refresh_payload, secret, algorithm='HS256'),
    )