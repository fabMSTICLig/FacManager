
from django.core.management.base import BaseCommand, CommandError
from django_caldav_event.models import CalendarInfos, CalDavEvent

class Command(BaseCommand):
    help = 'Sync caldav event on all calendars'
    
    def handle(self, *args, **options):

        calinfos = CalendarInfos.objects.all()

        for cal in calinfos:
            if cal.url:
                try:
                    cal.refresh()
                except:
                    print("Fail to refresh "+str(cal))

