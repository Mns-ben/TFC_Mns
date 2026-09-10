from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'          # <-- Important : le chemin complet
    verbose_name = "Observatoire Grand Inga"