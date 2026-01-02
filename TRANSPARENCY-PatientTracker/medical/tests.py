from django.test import TestCase
from .models import Triage
from visits.models import Visit
from patients.models import Patient

class TriageTest(TestCase):
    def test_save_vitals(self):
        # Simple Test: Can we save temperature?
        p = Patient.objects.create(first_name="A", last_name="B", date_of_birth="2000-01-01", national_id="123")
        v = Visit.objects.create(patient=p, visit_number="V-1")
        
        triage = Triage.objects.create(
            visit=v,
            temperature=37.5,
            systolic_bp=120,
            diastolic_bp=80,
            heart_rate=70,
            weight_kg=60
        )
        self.assertEqual(triage.temperature, 37.5)