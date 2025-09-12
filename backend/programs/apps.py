from django.apps import AppConfig


class ProgramsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'programs'

    def ready(self):
        # importe les signals pour qu'ils soient enregistrés
        import programs.signals  # noqa
