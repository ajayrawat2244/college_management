from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from core.models import TenantModel


class CourseContent(TenantModel):
    class ContentType(models.TextChoices):
        VIDEO = "VIDEO", "Video"
        PDF = "PDF", "PDF Notes"

    title = models.CharField(max_length=200)
    course = models.ForeignKey(
        "academy.Course",
        on_delete=models.CASCADE,
        related_name="contents"
    )
    content_type = models.CharField(max_length=10, choices=ContentType.choices)
    video_url = models.URLField(blank=True, null=True)
    pdf_notes = models.FileField(upload_to="course_notes/", blank=True, null=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.content_type == self.ContentType.VIDEO and not self.video_url:
            raise ValidationError({"video_url": "Video URL is required for video content."})

        if self.content_type == self.ContentType.PDF and not self.pdf_notes:
            raise ValidationError({"pdf_notes": "PDF file is required for PDF notes."})

        if self.video_url and self.content_type != self.ContentType.VIDEO:
            raise ValidationError({"video_url": "Video URL should only be set for video content."})

        if self.pdf_notes and self.content_type != self.ContentType.PDF:
            raise ValidationError({"pdf_notes": "PDF notes should only be set for PDF content."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ContentReview(TenantModel):
    content = models.ForeignKey(
        CourseContent,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="content_reviews"
    )
    rating = models.PositiveSmallIntegerField()
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("content", "student")
        ordering = ["-created_at"]

    def clean(self):
        if not (1 <= self.rating <= 5):
            raise ValidationError({"rating": "Rating must be between 1 and 5."})

        if self.content and self.student:
            if self.content.tenant_id != self.student.tenant_id:
                raise ValidationError("Student and content must belong to the same tenant.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.content} ({self.rating})"


class LiveClass(TenantModel):
    class Platform(models.TextChoices):
        ZOOM = "ZOOM", "Zoom"
        GOOGLE_MEET = "GOOGLE_MEET", "Google Meet"

    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    course = models.ForeignKey(
        "academy.Course",
        on_delete=models.CASCADE,
        related_name="live_classes"
    )
    title = models.CharField(max_length=200)
    platform = models.CharField(max_length=20, choices=Platform.choices)
    meeting_url = models.URLField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        now = timezone.now()

        if self.starts_at and self.starts_at <= now:
            raise ValidationError({"starts_at": "Meeting time has already passed."})

        if self.ends_at and self.starts_at and self.ends_at <= self.starts_at:
            raise ValidationError({"ends_at": "End time must be after start time."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.course.name}"