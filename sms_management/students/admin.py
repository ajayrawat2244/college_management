from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "enrollment_no", "tenant", "enrollment_date")
    search_fields = ("user__name", "enrollment_no")
    list_filter = ("tenant", "enrollment_date")

    fieldsets = (
        ("Basic Info", {
            "fields": ("user", "enrollment_no", "tenant")
        }),
        ("Enrollment", {
            "fields": ("enrollment_date",)
        }),
        ("Notification Settings", {
            "fields": (
                "email_notifications",
                "sms_notifications",
                "push_notifications",
            )
        }),
    )