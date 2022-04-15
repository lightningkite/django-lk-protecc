from django.apps import AppConfig
from django.db.models.signals import post_save


class ProteccConfig(AppConfig):
    name = 'django_lk_protecc.protecc'

    def ready(self):
        from . import signals
