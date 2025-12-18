from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from .models import Patient
from .serializers import PatientSerializer

# Patient ViewSet

class PatientViewSet(viewsets.ModelViewSet):
    # Order patients by creation date, newest first

    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer
    
    # Enable search functionality on specified fields
    
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name", "national_id", "phone"]

    # Prevent Delete operations on patients
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"error": "Security Alert: Medical records cannot be deleted. They are permanent."}, 
            status=status.HTTP_403_FORBIDDEN
        )