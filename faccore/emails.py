from collections import OrderedDict
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import email.utils
from ics import Calendar, Event

from .models import Reservation

class NotifEmails:
    
    @staticmethod
    def send_notif(reservation, user):
        """
        Send notification mail to the given user
        """
        status = str(OrderedDict(Reservation.STATUS)[reservation.status])
        startdate = reservation.start_date.strftime("%d/%m/%Y %H:%M:%S")
        context = {
                "reservation":reservation,
                "status": status,
                "startdate": startdate}
        subject = render_to_string(
            template_name='emails/updateresa_subject.txt',
            context=context
        ).strip()
        text_content = render_to_string(
            template_name='emails/updateresa_content.txt',
            context=context
        )
        html_content = render_to_string(
            template_name='emails/updateresa_content.html',
            context=context
        )
        msg = EmailMultiAlternatives(
                subject,
                text_content,
                email.utils.formataddr((
                    settings.LABNAME,
                    settings.EMAIL_SENDER)),
                [email.utils.formataddr((
                    user.first_name +
                    ' ' +
                    user.last_name, user.email))])
        msg.attach_alternative(html_content, "text/html")
        # print(msg.message())
        try:
            msg.send()
        except:
            print("fail to send notif to " + user.email)

    @staticmethod
    def send_admin_notif(reservation, user):
        """
        Send notification mail for the given user
        """
        startdate = reservation.start_date.strftime("%d/%m/%Y %H:%M:%S")
        enddate = reservation.end_date.strftime("%d/%m/%Y %H:%M:%S")
        context = {'SITE_URL': settings.SITE_URL,
                "reservation":reservation,
                "startdate": startdate,
                "enddate": enddate,
                }
        subject = render_to_string(
            template_name='emails/newresa_subject.txt',
            context=context
        ).strip()
        text_content = render_to_string(
            template_name='emails/newresa_content.txt',
            context=context
        )
        html_content = render_to_string(
            template_name='emails/newresa_content.html',
            context=context
        )
        sendto = [settings.EMAIL_ADMIN]
        if reservation.manager:
            sendto.append(reservation.manager.user.email)

        msg = EmailMultiAlternatives(
                subject,
                text_content,
                email.utils.formataddr((settings.LABNAME,
                    settings.EMAIL_SENDER)),
                [settings.EMAIL_ADMIN],
                reply_to=[email.utils.formataddr((user.first_name +
                    ' ' + user.last_name, user.email))])
        msg.attach_alternative(html_content, "text/html")

        c = Calendar()
        e = Event()
        e.name = str(reservation.user) +" "+ reservation.reservation_type.name
        e.begin = reservation.start_date.isoformat()
        e.end = reservation.end_date.isoformat()
        c.events.add(e)
        msg.attach("event.ics", c.serialize(),"text/calendar")
        #print(msg.message())
        try:
            msg.send()
        except:
            print("fail to send notif to " + str(sendto))

