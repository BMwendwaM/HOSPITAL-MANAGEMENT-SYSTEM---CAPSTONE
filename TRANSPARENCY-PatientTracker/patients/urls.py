from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet

# Create a router and register paths

router = DefaultRouter()
router.register(r'', PatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]