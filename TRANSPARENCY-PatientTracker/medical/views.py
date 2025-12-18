from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Triage, Diagnosis
from .serializers import TriageSerializer, DiagnosisSerializer
from visits.models import Visit

class TriageViewSet(viewsets.ModelViewSet):
    queryset = Triage.objects.all()
    serializer_class = TriageSerializer

    # When Nurse saves Triage, move patient to Consultation
    def perform_create(self, serializer):
        instance = serializer.save(nurse=self.request.user)
        
        # Find the visit and update status
        visit = instance.visit
        visit.status = Visit.Status.CONSULTATION
        visit.save()

class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer

    def perform_create(self, serializer):
        # Save the diagnosis instance
        instance = serializer.save(doctor=self.request.user)
        
        # After Diagnosis, move patient based on follow-up decision
        visit = instance.visit
        decision = instance.follow_up
        
        if decision == "lab":
            visit.status = Visit.Status.LAB
        elif decision == "radiology":
            visit.status = Visit.Status.RADIOLOGY
        elif decision == "pharmacy":
            visit.status = Visit.Status.PHARMACY
        else:
            # Default to billing if no follow-up
            visit.status = Visit.Status.BILLING
            
        visit.save()

        # Prevent Delete operations on triage and diagnosis records
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"error": "Security Alert: Medical records cannot be deleted. They are permanent."}, 
            status=status.HTTP_403_FORBIDDEN
        )
