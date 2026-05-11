from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from core.models import TenantModel


class GradingScheme(TenantModel):
    """
    One grading scheme per tenant or multiple schemes if needed.
    Example: Default UG Scheme, PG Scheme, etc.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class GradeRange(TenantModel):
    """
    Admin-defined score ranges:
    90-100 = A+
    80-89 = A
    etc.
    """
    scheme = models.ForeignKey(
        GradingScheme,
        on_delete=models.CASCADE,
        related_name="ranges"
    )
    grade_name = models.CharField(max_length=10)   # A+, A, B, etc.
    min_score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    grade_point = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
    is_passing = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-min_score", "order"]
        unique_together = ("scheme", "grade_name")

    def clean(self):
        if self.min_score < 0 or self.max_score > 100:
            raise ValidationError("Score range must be between 0 and 100.")

        if self.min_score > self.max_score:
            raise ValidationError("Minimum score cannot be greater than maximum score.")

        if self.scheme and self.tenant_id and self.scheme.tenant_id != self.tenant_id:
            raise ValidationError("Grade range and scheme must belong to the same tenant.")

        overlap_exists = GradeRange.objects.filter(
            tenant=self.tenant,
            scheme=self.scheme,
            min_score__lte=self.max_score,
            max_score__gte=self.min_score,
        )

        if self.pk:
            overlap_exists = overlap_exists.exclude(pk=self.pk)

        if overlap_exists.exists():
            raise ValidationError("This score range overlaps with an existing grade range.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.grade_name} ({self.min_score}-{self.max_score})"