from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Set up the router and register the paths

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]