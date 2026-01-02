from django.test import TestCase
from .models import Invoice
from visits.models import Visit
from patients.models import Patient

class BillingTest(TestCase):
    def test_create_invoice(self):
        # Simple Test: Can we create a bill?
        p = Patient.objects.create(first_name="A", last_name="B", date_of_birth="2000-01-01", national_id="123")
        v = Visit.objects.create(patient=p, visit_number="V-1")
        
        invoice = Invoice.objects.create(visit=v, total_amount=500.00)
        
        self.assertEqual(invoice.total_amount, 500.00)
        self.assertFalse(invoice.paid) # Invoices should be unpaid by default