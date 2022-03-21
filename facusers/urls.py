from django.urls import path, include
from .views import UserViewSet, SelfView, OrganizationViewSet, ProjectViewSet, RGPDAcceptView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('self/', SelfView.as_view()),
    path('self/rgpd/', RGPDAcceptView.as_view()),
]
