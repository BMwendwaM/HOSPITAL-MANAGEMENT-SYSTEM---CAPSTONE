from rest_framework import serializers
from .models import Patient

# Patient Serializer

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'