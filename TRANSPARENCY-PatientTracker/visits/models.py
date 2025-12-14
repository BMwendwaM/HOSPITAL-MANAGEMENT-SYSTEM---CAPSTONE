from django.db import models
from patients.models import Patient

# Visits Model for tracking patient visits status and details

class Visit(models.Model):

    class Status(models.TextChoices):
        WAITING = "waiting", "Waiting"
        TRIAGE = "triage", "In Triage"
        CONSULTATION = "consultation", "In Consultation"
        LAB = "lab", "In Laboratory"
        RADIOLOGY = "radiology", "In Radiology"
        PHARMACY = "pharmacy", "In Pharmacy"
        BILLING = "billing", "In Billing"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="visits"
    )

    visit_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WAITING
    )

    payment_type = models.CharField(
        max_length=20,
        choices=[
            ("cash", "Cash"),
            ("credit", "Credit"),
            ("insurance", "Insurance"),
        ]
    )

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Visit {self.visit_number} - {self.patient}"
