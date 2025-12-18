from django.db import models
from django.conf import settings
from visits.models import Visit

class Triage(models.Model):
    # One visit has exactly ONE triage record.

    visit = models.OneToOneField(Visit, on_delete=models.CASCADE, related_name="triage")
    nurse = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    # Vital Signs

    temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text="Degree Celsius")
    systolic_bp = models.IntegerField(help_text="Top number (mmHg)")
    diastolic_bp = models.IntegerField(help_text="Bottom number (mmHg)")
    heart_rate = models.IntegerField(help_text="BPM")
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vitals for Visit {self.visit.visit_number}"



class Diagnosis(models.Model):
    # A visit can have multiple diagnoses.
    
    visit = models.ForeignKey(Visit, on_delete=models.PROTECT, related_name="diagnoses")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    disease_name = models.CharField(max_length=255)
    symptoms = models.TextField()
    prescription = models.TextField(help_text="Medicines prescribed")
    lab_request = models.TextField(blank=True, help_text="Tests requested")

    # NEW FIELD: The Doctor's Decision
    FOLLOW_UP_CHOICES = [
        ("pharmacy", "Pharmacy"),
        ("lab", "Laboratory"),
        ("radiology", "Radiology"),
        ("billing", "Billing"),
    ]
    follow_up = models.CharField(max_length=20, choices=FOLLOW_UP_CHOICES, default="billing")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.disease_name} - {self.visit.patient.first_name}"