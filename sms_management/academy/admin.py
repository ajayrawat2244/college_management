from django.contrib import admin
from .models import CourseCategory, Subject, Course


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "tenant")
    search_fields = ("name",)
    list_filter = ("tenant",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "category", "tenant")
    search_fields = ("name", "code")
    list_filter = ("tenant", "category")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "tenant", "is_multilanguage")
    list_filter = ("tenant", "is_multilanguage", "primary_language")
    search_fields = ("name",)

    filter_horizontal = ("subjects",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "description", "category", "subjects", "tenant")
        }),
        ("Language Settings", {
            "fields": ("is_multilanguage", "primary_language", "supported_languages")
        }),
    )