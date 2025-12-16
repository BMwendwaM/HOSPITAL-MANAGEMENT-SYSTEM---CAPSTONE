from django.contrib import admin
from .models import Patient
from visits.models import Visit

# Inline admin for Visit

class VisitInline(admin.TabularInline):
    model = Visit
    extra = 1  # number of extra forms to show
    fields = ("visit_number", "status", "payment_type", "started_at", "completed_at")
    readonly_fields = ("visit_number", "started_at", "completed_at")  # make some fields read-only
    show_change_link = True  # link to the Visit change page

# Patient admin with Visits inline

class PatientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "date_of_birth", "gender")
    search_fields = ("first_name", "last_name")
    inlines = [VisitInline]

# Register models

admin.site.register(Patient, PatientAdmin)
admin.site.register(Visit)  # Register Visit model separately if needed
