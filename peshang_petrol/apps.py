from django.apps import AppConfig


class PeshangPetrolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'peshang_petrol'

    def ready(self):
        import peshang_petrol.signals
