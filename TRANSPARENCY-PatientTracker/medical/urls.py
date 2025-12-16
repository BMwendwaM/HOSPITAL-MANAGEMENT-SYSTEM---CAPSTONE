from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TriageViewSet, DiagnosisViewSet

router = DefaultRouter()
router.register(r'triage', TriageViewSet)
router.register(r'diagnosis', DiagnosisViewSet)

urlpatterns = [
    path('', include(router.urls)),
]