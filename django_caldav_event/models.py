from cryptography.fernet import Fernet
import base64
import caldav
from caldav.elements import cdav
from caldav.elements import dav
from django.db import models
from .app_settings import app_settings
from datetime import datetime
from datetime import timedelta

# Create your models here.


class CalendarInfos(models.Model):
    
    name = models.CharField(max_length=30)
    url = models.URLField(null=True, blank=True)
    login = models.CharField(max_length=50,null=True, blank=True)
    password_hash = models.CharField(max_length=255,null=True, blank=True)
    sync_token = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.name


    def refresh(self):
        
        if(self.url):
            f = Fernet(app_settings.CIPHER_KEY)
            passw = (base64.b64decode(f.decrypt(
                bytes(self.password_hash, encoding="ascii"))) if self.password_hash else None)
            with caldav.DAVClient(
                url=self.url,
                username=self.login,
                password=passw,
            ) as client:
                p = client.principal()
                calendar = p.calendar(cal_url=self.name)
                r_start = datetime.now()
                r_end = datetime.now()+timedelta(days = app_settings.REFRESH_WINDOW)
                events_fetched = calendar.search(
                    start=r_start,
                    end=r_end,
                    event=True,
                    expand=False,
                    props=[dav.GetEtag()]
                )
                evdict = {}
                for event in events_fetched:
                    evdict[event.props.get(dav.GetEtag.tag)]=event
                delevents = (CalDavEvent.objects
                    .filter(calendar=self)
                    .exclude(etag__in=list(evdict.keys())))
                delevents.delete()
                no_update_events = set(CalDavEvent.objects
                        .filter(calendar=self)
                        .filter(etag__in=list(evdict.keys()))
                        .values_list('etag', flat=True))
                update_tag = set(evdict.keys())-no_update_events
                for tag in update_tag:
                    newev = evdict[tag]
                    newev.expand_rrule(r_start,r_end)
                    for e in newev.split_expanded():
                        denv = CalDavEvent(calendar=self,
                            url=newev.url,
                            etag=tag,
                            summary=e.icalendar_component.get("summary"),
                            description=e.icalendar_component.get("description"),
                            dtstart=e.icalendar_component.get("dtstart").dt,
                            dtend=e.icalendar_component.get("dtend").dt
                            )
                        denv.save()


class CalDavEvent(models.Model):

    calendar = models.ForeignKey(CalendarInfos, on_delete=models.CASCADE)
    url = models.URLField()
    etag = models.CharField(max_length=30)
    dtstart = models.DateTimeField()
    dtend = models.DateTimeField()
    summary = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.etag+" "+self.summary
