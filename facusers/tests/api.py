"""
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
"""

import json
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from django.contrib.auth import get_user_model
from facusers.models import Project, Organization, OrganizationType
from facusers.views import UserViewSet, OrganizationViewSet, ProjectViewSet


class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fabuser = get_user_model().objects.create_user(
            username='fabmstic', first_name='admin', last_name="user", email='jacob@j.jj', password='top_secret', is_superuser=True, is_staff=True)
        cls.stauser = get_user_model().objects.create_user(
            username='standard', first_name='standard', last_name="user", email='jacob@j.jj', password='top_secret')
        cls.stauser.charter=True
        cls.stauser.save()

    def test_standard_user_list(self):
        user = get_user_model().objects.get(username='standard')
        api_request = APIRequestFactory().get("/api/users/")
        force_authenticate(api_request, user=user)
        list_view = UserViewSet.as_view({'get': 'list'})
        response = list_view(api_request)
        self.assertEqual(response.status_code, 403)

    def testSelfOrAdmin(self):
        user = get_user_model().objects.get(username='fabmstic')
        api_request = APIRequestFactory().get("/api/users/"+str(self.stauser.pk)+"/")
        force_authenticate(api_request, user=user)
        detail_view = UserViewSet.as_view({'get': 'retrieve'})
        response = detail_view(api_request, pk=self.stauser.pk)
        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.data)

        user = get_user_model().objects.get(username='standard')
        api_request = APIRequestFactory().get("/api/users/"+str(self.fabuser.pk)+"/")
        force_authenticate(api_request, user=user)
        response = detail_view(api_request, pk=self.fabuser.pk)
        self.assertEqual(response.status_code, 403)

        api_request = APIRequestFactory().get("/api/users/"+str(self.stauser.pk)+"/")
        force_authenticate(api_request, user=user)
        response = detail_view(api_request, pk=self.stauser.pk)
        self.assertEqual(response.status_code, 200)

    def testUpdate(self):

        user = get_user_model().objects.get(username='standard')
        api_request = APIRequestFactory().get("/api/users/"+str(self.stauser.pk)+"/")
        force_authenticate(api_request, user=user)
        detail_view = UserViewSet.as_view({'get': 'retrieve'})
        responseuser = detail_view(api_request, pk=self.stauser.pk)
        userdata = json.loads(json.dumps(responseuser.data))
        userdata['email'] = 'j.j@j.jj'

        api_request = APIRequestFactory().put("/api/users/"+str(self.stauser.pk)+"/", userdata, format='json')
        force_authenticate(api_request, user=user)
        update_view = UserViewSet.as_view({'put': 'update'})
        response = update_view(api_request, pk=self.stauser.pk)
        self.assertEqual(response.status_code, 200)

    def testUpdateOtherUser(self):

        user = get_user_model().objects.get(username='standard')
        api_request = APIRequestFactory().get("/api/users/"+str(self.stauser.pk)+"/")
        force_authenticate(api_request, user=user)
        detail_view = UserViewSet.as_view({'get': 'retrieve'})
        responseuser = detail_view(api_request, pk=self.stauser.pk)
        userdata = json.loads(json.dumps(responseuser.data))
        userdata['email'] = 'j.j@j.jj'

        api_request = APIRequestFactory().put("/api/users/"+str(self.fabuser.pk)+"/", userdata, format='json')
        force_authenticate(api_request, user=user)
        update_view = UserViewSet.as_view({'put': 'update'})
        response = update_view(api_request, pk=self.fabuser.pk)
        self.assertEqual(response.status_code, 403)



    def testNewUser(self):
        api_request = APIRequestFactory().post("/api/users/create_user/",
                                               {'first_name': 'test', 'last_name': 'userlongname', 'email': 't@t.tt'})
        
        user = get_user_model().objects.get(username='standard')
        force_authenticate(api_request, user=user)
        create_view = UserViewSet.as_view({'post': 'create_user'})
        response = create_view(api_request)
        self.assertEqual(response.status_code, 403)

        user = get_user_model().objects.get(username='fabmstic')
        force_authenticate(api_request, user=user)
        create_view = UserViewSet.as_view({'post': 'create_user'})
        response = create_view(api_request)
        self.assertEqual(response.status_code, 200)

    def testNewUserUsername(self):
        #test two identical username, append number
        api_request = APIRequestFactory().post("/api/users/create_user/",
                                               {'first_name': 'Test', 'last_name': 'userlongname', 'email': 't@t.tt'})
        user = get_user_model().objects.get(username='fabmstic')
        force_authenticate(api_request, user=user)
        create_view = UserViewSet.as_view({'post': 'create_user'})
        response = create_view(api_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('username'), "userlont")
        response = create_view(api_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('username'), "userlont2")

class OrgaTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.fabuser = get_user_model().objects.create_user(
            username='fabmstic', email='jacob@…', password='top_secret', is_superuser=True, is_staff=True)
        cls.stauser = get_user_model().objects.create_user(
            username='standard', email='jacob@…', password='top_secret')
        cls.stauser.charter=True
        cls.stauser.save()
        cls.orga = Organization(name="lig", contact="lig@l.ll")
        cls.orga.save()


    def testSerializerType(self):
        user = get_user_model().objects.get(username='fabmstic')
        api_request = APIRequestFactory().get("api/organizations/"+str(self.orga.pk)+"/")
        force_authenticate(api_request, user=user)
        detail_view = OrganizationViewSet.as_view({'get': 'retrieve'})
        response = detail_view(api_request, pk=self.orga.pk)
        self.assertEqual(response.status_code, 200)
        self.assertIn('contact', response.data)

        user = get_user_model().objects.get(username='standard')
        api_request = APIRequestFactory().get("api/organizations/"+str(self.orga.pk)+"/")
        force_authenticate(api_request, user=user)
        detail_view = OrganizationViewSet.as_view({'get': 'retrieve'})
        response = detail_view(api_request, pk=self.orga.pk)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('contact', response.data)

class ProjectTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.fabuser = get_user_model().objects.create_user(
            username='fabmstic', email='jacob@…', password='top_secret', is_superuser=True, is_staff=True)
        cls.stauser = get_user_model().objects.create_user(
            username='standard', email='jacob@…', password='top_secret')
        cls.stauser.charter=True
        cls.stauser.save()
        cls.project = Project(name="lig2021")
        cls.project.save()


    def testProjectVisibility(self):
        user = get_user_model().objects.get(username='standard')
        api_request = APIRequestFactory().get("api/projects/")
        force_authenticate(api_request, user=user)
        list_view = ProjectViewSet.as_view({'get': 'list'})
        response = list_view(api_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, response.data['count'])

        self.project.members.add(self.stauser)

        user = get_user_model().objects.get(username='standard')
        api_request = APIRequestFactory().get("api/projects/")
        force_authenticate(api_request, user=user)
        list_view = ProjectViewSet.as_view({'get': 'list'})
        response = list_view(api_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, response.data['count'])
