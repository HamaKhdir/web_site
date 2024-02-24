from django.apps import AppConfig


class AwatPetrolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'awat_petrol'

    def ready(self):
        import awat_petrol.signals
