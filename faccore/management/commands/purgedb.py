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

import datetime

from faccore.models import Reservation


class Command(BaseCommand):
    help = 'Purge the database from old reservation'

    def add_arguments(self, parser):
        parser.add_argument("date", type=str)

    def handle(self, *args, **options):
        purgedate = datetime.date.fromisoformat(options["date"])
        print(purgedate)
        print(Reservation.objects.filter(start_date__lte = purgedate).delete())
