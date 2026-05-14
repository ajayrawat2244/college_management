# core/models.py
from django.db import models
from django.core.exceptions import ValidationError
from core.managers import TenantManager, TenantQuerySet


class TenantModel(models.Model):
    tenant = models.ForeignKey("tenants.College", on_delete=models.CASCADE, related_name="%(class)ss", db_index=True)

    objects = TenantManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if not self.tenant_id:
            raise ValidationError({"tenant": "Tenant is required."})