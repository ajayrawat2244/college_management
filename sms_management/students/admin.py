from django.contrib import admin
from .models import Student, Enquiry


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "enrollment_no",
        "tenant",
        "enrollment_date",
    )

    search_fields = (
        "user__email",
        "enrollment_no",
    )

    list_filter = (
        "tenant",
        "enrollment_date",
    )

    readonly_fields = (
        "enrollment_date",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "user",
                    "tenant",
                    "enrollment_no",
                )
            },
        ),

        (
            "Notification Preferences",
            {
                "fields": (
                    "email_notifications",
                    "sms_notifications",
                    "push_notifications",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "enrollment_date",
                )
            },
        ),
    )


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "phone",
        "tenant",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
    )

    list_filter = (
        "tenant",
        "created_at",
    )