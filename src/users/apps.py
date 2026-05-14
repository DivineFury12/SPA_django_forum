import django.apps


class UsersConfig(django.apps.AppConfig):
    name = 'users'

    def ready(self):
        import users.signals