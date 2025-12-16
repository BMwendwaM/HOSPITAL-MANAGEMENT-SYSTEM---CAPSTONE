from django.db import models
from patients.models import Patient
from django.utils import timezone

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
        on_delete=models.PROTECT,
        related_name="visits"
    )

    visit_number = models.CharField(max_length=20, unique=True, blank=True)
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

    def save(self, *args, **kwargs):
        if not self.visit_number:
            today = timezone.now().date()
            # Count how many visits exist today
            today_count = Visit.objects.filter(started_at__date=today).count() + 1
            # Format: VST-YYYYMMDD-XXX
            self.visit_number = f"VST-{today.strftime('%Y%m%d')}-{today_count:03}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Visit {self.visit_number} - {self.patient}"