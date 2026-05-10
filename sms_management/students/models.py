from django.db import models
from core.models import TenantModel
from core.managers import TenantManager
from core.utils import get_current_tenant


class Student(TenantModel):

    objects = TenantManager()

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    enrollment_no = models.CharField(max_length=50, unique=True)
    enrollment_date = models.DateField(auto_now_add=True)

    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name} - {self.enrollment_no}"

    def save(self, *args, **kwargs):
        if not self.tenant_id:
            self.tenant = get_current_tenant()

        super().save(*args, **kwargs)
