from django.conf import settings
from datetime import time

class AppSettings:
    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        return getattr(settings, self.prefix + name, dflt)

    @property
    def BUSINESS_HOURS(self):
        """Dictionary to oppening hours"""
        """Key is day of the week 1=Monday"""
        hours=[
                {
                'days_of_week' : [1,2,3,4,5],
                'start_time': time(9,00),
                'end_time': time(11,30),
                },
                {
                'days_of_week' : [1,2,3,4,5],
                'start_time': time(13,30),
                'end_time': time(17,00),
                }
            ]

        return self._setting("BUSINESS_HOURS", hours)

app_settings = AppSettings("FACCORE_")
