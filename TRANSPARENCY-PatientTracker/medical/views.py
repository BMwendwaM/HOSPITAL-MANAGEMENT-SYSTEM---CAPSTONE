from rest_framework import viewsets
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
        
        if decision == 'lab':
            visit.status = Visit.Status.LAB
        elif decision == 'radiology':
            visit.status = Visit.Status.RADIOLOGY
        elif decision == 'pharmacy':
            visit.status = Visit.Status.PHARMACY
        else:
            # Default to billing if no follow-up
            visit.status = Visit.Status.BILLING
            
        visit.save()