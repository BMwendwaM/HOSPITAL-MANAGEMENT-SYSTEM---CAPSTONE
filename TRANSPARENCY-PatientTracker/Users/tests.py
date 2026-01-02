from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTest(TestCase):
    def test_create_user(self):
        # Simple Test: Can we create a nurse?
        user = User.objects.create_user(username="nurse1", role="NURSE")
        self.assertEqual(user.username, "nurse1")
        self.assertEqual(user.role, "NURSE")