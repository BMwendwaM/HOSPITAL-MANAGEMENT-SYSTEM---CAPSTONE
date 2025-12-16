from django.db import models
from visits.models import Visit

class Invoice(models.Model):
    visit = models.OneToOneField(Visit, on_delete=models.PROTECT, related_name="invoice")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.id} for Visit {self.visit.visit_number}"

class BillItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name="items")
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.description}: {self.amount}"