from rest_framework import serializers
from .models import Visit
from patients.serializers import PatientSerializer
from medical.serializers import TriageSerializer, DiagnosisSerializer
from billing.serializers import InvoiceSerializer

# Visit Serializer

class VisitSerializer(serializers.ModelSerializer):
    # Show detailed patient information
    
    patient_data = PatientSerializer(source="patient", read_only=True)
    triage = TriageSerializer(read_only=True)
    diagnoses = DiagnosisSerializer(many=True, read_only=True)

    # Attach the billing invoice details
    
    invoice = InvoiceSerializer(read_only=True)

    class Meta:
        model = Visit
        fields = [
            "id", "visit_number", "status", "patient", "patient_data", 
            "payment_type", "started_at", "triage", "diagnoses", "invoice"
        ]
        read_only_fields = ['visit_number', 'started_at', 'completed_at']