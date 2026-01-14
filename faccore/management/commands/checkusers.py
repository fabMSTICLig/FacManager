"""
Copyright (C) 2020-2026 LIG Université Grenoble Alpes


This file is part of FacManager.

Matos is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
"""
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Q
from django_auth_ldap.backend import LDAPBackend

import datetime

from facusers.models import User
from faccore.models import Reservation


class Command(BaseCommand):
    help = 'Check users from ldap server, if deleted user reservation go to anonymous user.'

    def handle(self, *args, **options):
        oldusers=[]
        anonuser=User.objects.get(username="anonymous")
        for user in User.objects.exclude(username="anonymous").filter(password=''):
            userldap = LDAPBackend().populate_user(user.username)
            if(userldap is None):
                oldusers.append(user.id)
        Reservation.objects.filter(user__in=oldusers).update(user=anonuser)
        User.objects.filter(id__in=oldusers).delete()
