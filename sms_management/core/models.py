from django.db import models

class TenantModel(models.Model):
    tenant = models.ForeignKey(
        "tenants.College",
        on_delete=models.CASCADE,
        related_name="%(class)ss"
    )

    class Meta:
        abstract = True