from django.contrib import admin
from .models import Patient

# Register the Patient model to make it accessible via the admin

admin.site.register(Patient)
