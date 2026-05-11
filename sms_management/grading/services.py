from decimal import Decimal

from .models import GradeRange


def get_grade_for_score(score, tenant, scheme=None):
    """
    Returns the matching GradeRange for a given score.
    Example:
    score = 92 -> A+
    """
    score = Decimal(str(score))

    queryset = GradeRange.objects.filter(
        tenant=tenant,
        scheme=scheme
    ) if scheme else GradeRange.objects.filter(tenant=tenant)

    return queryset.filter(
        min_score__lte=score,
        max_score__gte=score
    ).first()


def get_grade_label(score, tenant, scheme=None):
    grade = get_grade_for_score(score, tenant, scheme=scheme)
    return grade.grade_name if grade else None