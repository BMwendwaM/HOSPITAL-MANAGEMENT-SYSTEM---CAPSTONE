from django.db import models
from django.contrib.auth.models import AbstractUser


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    class Roles(models.TextChoices):
        RECEPTIONIST = "receptionist", "Receptionist"
        CASHIER = "cashier", "Cashier"
        NURSE = "nurse", "Nurse"
        DOCTOR = "doctor", "Doctor"
        LAB_TECH = "lab_tech", "Lab Technician"
        RADIOLOGIST = "radiologist", "Radiologist"
        PHARMACIST = "pharmacist", "Pharmacist"
        ADMINISTRATOR = "administrator", "Hospital Administrator"

    role = models.CharField(max_length=30, choices=Roles.choices, default=Roles.RECEPTIONIST)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

