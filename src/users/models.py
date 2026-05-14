import django.db.models
import django.conf


class Profile(django.db.models.Model):
    user = django.db.models.OneToOneField(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name='profile',
    )
    nickname = django.db.models.CharField(max_length=64, blank=True)
    avatar   = django.db.models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} profile'