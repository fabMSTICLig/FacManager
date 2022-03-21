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
