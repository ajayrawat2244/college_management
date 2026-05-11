from django.contrib import admin
from .models import CourseContent, ContentReview, LiveClass


@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "content_type", "tenant", "is_published", "order")
    list_filter = ("tenant", "content_type", "is_published")
    search_fields = ("title", "course__name")
    ordering = ("order", "created_at")


@admin.register(ContentReview)
class ContentReviewAdmin(admin.ModelAdmin):
    list_display = ("content", "student", "rating", "tenant", "created_at")
    list_filter = ("tenant", "rating", "created_at")
    search_fields = ("content__title", "student__user__name", "student__user__email")


@admin.register(LiveClass)
class LiveClassAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "platform", "starts_at", "status", "tenant")
    list_filter = ("tenant", "platform", "status")
    search_fields = ("title", "course__name")
    ordering = ("starts_at",)