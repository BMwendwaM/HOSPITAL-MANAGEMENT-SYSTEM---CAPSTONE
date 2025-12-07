from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Department

# Register User model

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Hospital Info", {"fields": ("role", "department", "phone")}),
    )
    list_display = ("username", "email", "role", "department", "is_staff")
    list_filter = ("role", "department", "is_staff", "is_superuser")