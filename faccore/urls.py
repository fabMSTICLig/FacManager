"""
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
"""

from rest_framework_nested import routers
from django.urls import path, include
from django.conf import settings
from .views import SupplyViewSet, SupplyUsageViewSet, MachineModelViewSet, ManagerViewSet, MachineViewSet, AvailabilityViewSet, ReservationTypeViewSet, ReservationViewSet, EventViewSet, TrainingLevelView, RefreshResourcesView, UsagesView

router = routers.DefaultRouter()
router.register(r'supplies', SupplyViewSet)
router.register(r'machine_models', MachineModelViewSet)
router.register(r'managers', ManagerViewSet)
router.register(r'machines', MachineViewSet)
router.register(r'availabilities', AvailabilityViewSet)
router.register(r'reservation_types', ReservationTypeViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'events', EventViewSet)

router_resa = routers.NestedSimpleRouter(router, r'reservations', lookup='resa')
router_resa.register(r'supply_usages', SupplyUsageViewSet, basename='supply_usages')

urlpatterns = [
    path('refresh/', RefreshResourcesView.as_view()),
    path('usages/', UsagesView.as_view()),
    path('users/<int:user_pk>/training_levels/', TrainingLevelView.as_view()),
    path('', include(router.urls)),
    path('', include(router_resa.urls)),
]


# Add an ical view if django-cal is installed
if 'django_ical' in settings.INSTALLED_APPS:
    from .views import ReservationsCal

    urlpatterns.append(path('cal/event.ics', ReservationsCal()))
