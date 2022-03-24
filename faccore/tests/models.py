"""
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import connection
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from faccore.models import *
from faccore.views import *
from datetime import datetime, timedelta
import json

class ReservationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fabuser = get_user_model().objects.create_user(
            username='fabmstic', email='admin@ttt.fr', password='top_secret', is_superuser=True, is_staff=True)
        cls.stauser = get_user_model().objects.create_user(
            username='standard', email='jacob@ttt.fr', password='top_secret')
        cls.stauser.charter=True
        cls.stauser.save()

        cls.mc3d = MachineCategory(name="3D printer")
        cls.mc3d.save()
        cls.mclaser = MachineCategory(name="laser")	
        cls.mclaser.save()
        cls.mmum2 = MachineModel(name="UM2E", category=cls.mc3d)
        cls.mmum2.save()
        cls.mmum3 = MachineModel(name="UM3E", category=cls.mc3d)
        cls.mmum3.save()
        cls.mmtro = MachineModel(name="Trotec 300", category=cls.mclaser)
        cls.mmtro.save()

        cls.mum21 = Machine(name="UM2E 1", model=cls.mmum2)
        cls.mum21.save()
        cls.mum22 = Machine(name="UM2E 2", model=cls.mmum2)
        cls.mum22.save()
        cls.mum31 = Machine(name="UM2E 1", model=cls.mmum3)
        cls.mum31.save()
        cls.mtro1 = Machine(name="Trotec 1", model=cls.mmtro)
        cls.mtro1.save()

        cls.man1 = Manager(name="germain", email="g@g.gg")
        cls.man1.save()
        cls.man2 = Manager(name="jerome", email="j@j.jj")
        cls.man2.save()

        cls.restytrain3d= ReservationType(name="Training 3D Printer",need_manager=True)
        cls.restytrain3d.save()
        cls.restytrain3d.needs.add(cls.mmum2)
        cls.restytrain3d.save()
        cls.restylaser= ReservationType(name="Laser",need_manager=False)
        cls.restylaser.save()
        cls.restylaser.needs.add(cls.mmtro)
        cls.restylaser.save()

    def test_reservation_standard_create(self):
        settings.DEBUG = True
        user = get_user_model().objects.get(username='standard')

        av = Availability(start_date="2019-07-04T12:30:00.000000Z",
                          end_date="2019-07-04T17:30:00.000000Z")
        av.save()
        av.ressources.add(self.man1)
        av.ressources.add(self.mum21)
        av.save()
        # Test normale create
        api_request = APIRequestFactory().post("/api/reservations/",
                {'user':user.id,'reservation_type': self.restytrain3d.pk, 'start_date': '2019-07-04T13:30:00.000000Z', 'end_date': '2019-07-04T16:30:00.000000Z', 'manager': self.man1.pk, 'uses': [self.mum21.pk]})
        force_authenticate(api_request, user=user)
        create_view = ReservationViewSet.as_view({'post': 'create'})
        response = create_view(api_request)
        self.assertEqual(response.status_code, 201)
        # Test standard fail change status
        api_request = APIRequestFactory().post("/api/reservations/",
                                               {'user':user.id, 'reservation_type': self.restytrain3d.pk, 'start_date': '2019-07-04T14:30:00.000000Z', 'end_date': '2019-07-04T16:30:00.000000Z', 'status': 'Accepted', 'manager': self.man1.pk, 'uses': [self.mum21.pk]})
        force_authenticate(api_request, user=user)
        create_view = ReservationViewSet.as_view({'post': 'create'})
        response = create_view(api_request)
        self.assertEqual(response.status_code, 403)
    
    def test_reservation_standard_create_noavail(self):
        settings.DEBUG = True
        user = get_user_model().objects.get(username='standard')

        av = Availability(start_date="2019-07-04T12:30:00.000000Z",
                          end_date="2019-07-04T17:30:00.000000Z")
        av.save()
        av.ressources.add(self.man1)
        av.ressources.add(self.mum21)
        av.save()
        # Test normale create
        api_request = APIRequestFactory().post("/api/reservations/",
                                               {'reservation_type': self.restytrain3d.pk, 'start_date': '2019-07-04T11:30:00.000000Z', 'end_date': '2019-07-04T16:30:00.000000Z', 'manager': self.man1.pk, 'uses': [self.mum21.pk]})
        force_authenticate(api_request, user=user)
        create_view = ReservationViewSet.as_view({'post': 'create'})
        response = create_view(api_request)
        self.assertEqual(response.status_code, 400)

    def test_reservation_forbid_standard_update_other(self):

        user = get_user_model().objects.get(username='fabmstic')
        api_request = APIRequestFactory().post("/api/reservations/",
                {'reservation_type': self.restytrain3d.pk, 'user':self.fabuser.pk, 'start_date': '2019-07-04T14:30:00.000000Z', 'end_date': '2019-07-04T16:30:00.000000Z', 'manager': self.man1.pk, 'uses': [self.mum21.pk]})
        force_authenticate(api_request, user=user)
        create_view = ReservationViewSet.as_view({'post': 'create'})
        response = create_view(api_request)
        self.assertEqual(response.status_code, 201)
        resid = str(response.data['id'])
        # Update someone else
        user = get_user_model().objects.get(username='standard')
        api_request = APIRequestFactory().put("/api/reservations/"+resid,
                                               {'reservation_type': self.restytrain3d.pk, 'start_date': '2019-07-04T14:30:00.000000Z', 'end_date': '2019-07-04T16:30:00.000000Z', 'manager': self.man1.pk, 'uses': [self.mum22.pk]})
        force_authenticate(api_request, user=user)
        create_view = ReservationViewSet.as_view({'put': 'update'})
        response = create_view(api_request, pk=resid)
        self.assertEqual(response.status_code, 403)

    def test_reservation_forbid_standard_update_accepted(self):

        user = get_user_model().objects.get(username='fabmstic')
        userstand = get_user_model().objects.get(username='standard')
        api_request = APIRequestFactory().post("/api/reservations/",
                                               {'reservation_type': self.restytrain3d.pk, 'user':self.stauser.pk, 'start_date': '2019-07-04T13:30:00.000000Z', 'end_date': '2019-07-04T16:30:00.000000Z', 'status': 'Accepted', 'manager': self.man1.pk, 'uses': [self.mum22.pk]})
        force_authenticate(api_request, user=user)
        create_view = ReservationViewSet.as_view({'post': 'create'})
        response = create_view(api_request)
        self.assertEqual(response.status_code, 201)
        resid = str(response.data['id'])

        user = get_user_model().objects.get(username='standard')
        api_request = APIRequestFactory().put("/api/reservations/"+resid,
                                              {'reservation_type': '4', 'start_date': '2019-07-04T14:30:00.000000Z', 'end_date': '2019-07-04T16:30:00.000000Z', 'manager': self.man1.pk, 'uses': [self.mum21.pk]})
        force_authenticate(api_request, user=user)
        create_view = ReservationViewSet.as_view({'put': 'update'})
        response = create_view(api_request, pk=resid)
        self.assertEqual(response.status_code, 403)

    def test_reservation_conflict(self):

        user = get_user_model().objects.get(username='fabmstic')
        # Test normale create
        api_request = APIRequestFactory().post("/api/reservations/",
                                               {'reservation_type': self.restytrain3d.pk, 'user':self.stauser.pk, 'start_date': '2019-07-04T13:30:00.000000Z', 'end_date': '2019-07-04T16:30:00.000000Z', 'status': 'Accepted', 'manager': self.man1.pk, 'uses': [self.mum22.pk]})
        force_authenticate(api_request, user=user)
        create_view = ReservationViewSet.as_view({'post': 'create'})
        response = create_view(api_request)
        self.assertEqual(response.status_code, 201)
        # Test conflict create
        api_request = APIRequestFactory().post("/api/reservations/",
                                               {'reservation_type': self.restytrain3d.pk, 'user':self.stauser.pk, 'start_date': '2019-07-04T14:30:00.000000Z', 'end_date': '2019-07-04T16:30:00.000000Z', 'status': 'Accepted', 'manager': self.man2.pk, 'uses': [self.mum22.pk]})
        force_authenticate(api_request, user=user)
        create_view = ReservationViewSet.as_view({'post': 'create'})
        response = create_view(api_request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['non_field_errors'][0], "Conflict using ressource UM2E UM2E 2")
        # Test conflict manager create
        api_request = APIRequestFactory().post("/api/reservations/",
                                               {'reservation_type': self.restytrain3d.pk, 'user':self.stauser.pk, 'start_date': '2019-07-04T14:30:00.000000Z', 'end_date': '2019-07-04T16:30:00.000000Z', 'status': 'Accepted', 'manager': self.man1.pk, 'uses': [self.mum21.pk]})
        force_authenticate(api_request, user=user)
        create_view = ReservationViewSet.as_view({'post': 'create'})
        response = create_view(api_request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['non_field_errors'][0], "germain is not available")

    def test_reservation_manager(self):

        user = get_user_model().objects.get(username='fabmstic')
        # test missing manager
        api_request = APIRequestFactory().post("/api/reservations/",
                                               {'reservation_type': self.restytrain3d.pk, 'user':self.stauser.pk, 'start_date': '2019-07-04T14:30:00.000000Z', 'end_date': '2019-07-04T16:30:00.000000Z', 'status': 'Accepted', 'manager': '', 'uses': [self.mum21.pk]})
        force_authenticate(api_request, user=user)
        create_view = ReservationViewSet.as_view({'post': 'create'})
        response = create_view(api_request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['non_field_errors'][0], "One manager is needed")
        # test not manager not needed
        api_request = APIRequestFactory().post("/api/reservations/",
                                               {'reservation_type': self.restylaser.pk, 'user':self.stauser.pk, 'start_date': '2019-07-04T14:30:00.000000Z', 'end_date': '2019-07-04T16:30:00.000000Z', 'status': 'Accepted', 'manager': self.man1.pk, 'uses': [self.mtro1.pk]})
        force_authenticate(api_request, user=user)
        create_view = ReservationViewSet.as_view({'post': 'create'})
        response = create_view(api_request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['non_field_errors'][0], "Manager is not needed")

    def test_reservation_wrong_machine(self):
        user = get_user_model().objects.get(username='fabmstic')
        api_request = APIRequestFactory().post("/api/reservations/",
                                               {'reservation_type': self.restytrain3d.pk, 'user':self.stauser.pk, 'start_date': '2019-07-04T14:30:00.000000Z', 'end_date': '2019-07-04T16:30:00.000000Z', 'status': 'Accepted', 'manager': self.man1.pk, 'uses': [self.mtro1.pk]})
        force_authenticate(api_request, user=user)
        create_view = ReservationViewSet.as_view({'post': 'create'})
        response = create_view(api_request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['non_field_errors'][0], "One instance of UM2E is needed")

    def test_reservation_missing_machine(self):
        user = get_user_model().objects.get(username='fabmstic')
        api_request = APIRequestFactory().post("/api/reservations/",
                                               {'reservation_type': self.restytrain3d.pk, 'user':self.stauser.pk, 'start_date': '2019-07-04T14:30:00.000000Z', 'end_date': '2019-07-04T16:30:00.000000Z', 'status': 'Accepted', 'manager': self.man1.pk, 'uses': []})
        force_authenticate(api_request, user=user)
        create_view = ReservationViewSet.as_view({'post': 'create'})
        response = create_view(api_request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['non_field_errors'][0], "One instance of UM2E is needed")

