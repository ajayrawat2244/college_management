from django.db import models
from django.utils import timezone

from .models import FeeInstallment


def get_overdue_installments(student, as_of=None):
    """
    Returns a queryset of overdue installments for a student.
    Overdue means:
    - due_date is before today's date
    - installment is not fully paid
    """
    if as_of is None:
        as_of = timezone.localdate()

    return FeeInstallment.objects.filter(
        fee_record__student=student,
        due_date__lt=as_of,
    ).exclude(
        status=FeeInstallment.Status.PAID
    ).filter(
        paid_amount__lt=models.F("amount")
    )


def has_overdue_installments(student, as_of=None):
    # Returns True if the student has any overdue installments.
    return get_overdue_installments(student, as_of=as_of).exists()