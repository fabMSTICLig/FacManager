from django.apps import AppConfig


class FacusersConfig(AppConfig):
    name = 'facusers'

    def ready(self):
        import facusers.signals
