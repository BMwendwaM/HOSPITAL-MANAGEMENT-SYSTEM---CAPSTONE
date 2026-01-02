from django.test import TestCase
from .models import Patient

class PatientTest(TestCase):
    def test_create_patient(self):
        # Simple Test: Can we register a patient?
        patient = Patient.objects.create(
            first_name="John", 
            last_name="Doe", 
            date_of_birth="1990-01-01", 
            gender="M", 
            national_id="123"
        )
        self.assertEqual(patient.first_name, "John")