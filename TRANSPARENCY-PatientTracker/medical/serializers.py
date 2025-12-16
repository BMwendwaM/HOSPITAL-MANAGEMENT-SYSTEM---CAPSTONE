from rest_framework import serializers
from .models import Triage, Diagnosis

class TriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Triage
        fields = '__all__'

        # Nurse is auto-filled by the logged-in user
        read_only_fields = ['nurse', 'created_at']

class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'

        # Doctor is auto-filled by the logged-in user
        read_only_fields = ['doctor', 'created_at']