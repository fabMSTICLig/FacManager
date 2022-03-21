from django.apps import AppConfig


class FaccoreConfig(AppConfig):
    name = 'faccore'

    def ready(self):
        import faccore.signals
