from django.apps import AppConfig


class PopulatedbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'populateDB'
    def ready(self):
        from . import signals