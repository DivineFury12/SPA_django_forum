import django.db.models.signals
import django.dispatch
import django.contrib.auth.models
import users.models


@django.dispatch.receiver(django.db.models.signals.post_save, sender=django.contrib.auth.models.User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        users.models.Profile.objects.create(user=instance)