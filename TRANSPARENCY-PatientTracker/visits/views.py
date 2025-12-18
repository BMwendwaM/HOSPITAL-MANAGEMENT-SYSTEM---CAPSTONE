from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Visit
from .serializers import VisitSerializer

# Visit ViewSet

class VisitViewSet(viewsets.ModelViewSet):
    # Order visits by start date, newest first

    queryset = Visit.objects.all().order_by("-started_at")
    serializer_class = VisitSerializer
    
    # Enable filtering on specified fields

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "patient__national_id", "visit_number"]

    def perform_create(self, serializer):
        # Set default status to WAITING on visit creation
        
        serializer.save(status=Visit.Status.WAITING)


    # Prevent Delete operations on visits
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"error": "Security Alert: Medical records cannot be deleted. They are permanent."}, 
            status=status.HTTP_403_FORBIDDEN
        )