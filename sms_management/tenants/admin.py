from django.contrib import admin
from .models import College


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ("name", "subdomain", "domain", "is_active", "created_at")
    search_fields = ("name", "subdomain", "domain", "email", "phone")
    list_filter = ("is_active", "created_at")
    ordering = ("name",)
    prepopulated_fields = {"subdomain": ("name",)}