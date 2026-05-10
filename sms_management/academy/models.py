from django.db import models
from core.models import TenantModel


class CourseCategory(TenantModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Subject(TenantModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    category = models.ForeignKey(
        CourseCategory,
        on_delete=models.CASCADE,
        related_name="subjects"
    )

    def __str__(self):
        return f"{self.name} ({self.code})"


class Course(TenantModel):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    category = models.ForeignKey(
        CourseCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses"
    )

    subjects = models.ManyToManyField(Subject, related_name="courses")

    # Language Management Toggle
    is_multilanguage = models.BooleanField(default=False)

    # Default language
    primary_language = models.CharField(
        max_length=50,
        default="English"
    )

    # Optional supported languages (JSON for flexibility)
    supported_languages = models.JSONField(
        default=list,
        blank=True,
        help_text="List of supported languages if multilanguage is enabled"
    )

    def get_languages(self):
        if self.is_multilanguage:
            return self.supported_languages
        return [self.primary_language]

    def __str__(self):
        return self.name