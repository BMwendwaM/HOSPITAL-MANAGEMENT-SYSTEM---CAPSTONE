from django.test import TestCase
from .models import Visit
from patients.models import Patient

class VisitTest(TestCase):
    def test_visit_default_status(self):
        # Simple Test: Does a new visit start as 'WAITING'?
        p = Patient.objects.create(first_name="Test", last_name="User", date_of_birth="2000-01-01", national_id="123")
        
        visit = Visit.objects.create(patient=p, visit_number="V-100")
        
        # This proves your logic works
        self.assertEqual(visit.status, "waiting")