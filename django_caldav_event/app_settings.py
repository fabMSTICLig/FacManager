from django.conf import settings


class AppSettings:
    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        return getattr(settings, self.prefix + name, dflt)

    @property
    def CIPHER_KEY(self):
        """KEY to cipher calendar password"""
        return self._setting("CYPHER_KEY", b'1xrsuoE9wElGsaSbItRkpgn5OjLKEhLWSnWcOQlSGy4=')

    @property
    def REFRESH_WINDOW(self):
        """Size of the time widows of a refresh in days"""
        return self._setting("REFRESH_WINDOW", 21)

app_settings = AppSettings("CALEVENT_")
