from django.db import models
from .utils import get_current_tenant


class TenantQuerySet(models.QuerySet):
    def for_tenant(self, tenant=None):
        tenant = tenant or get_current_tenant()
        if tenant is None:
            return self.none()
        return self.filter(tenant=tenant)


class TenantManager(models.Manager):
    def get_queryset(self):
        tenant = get_current_tenant()
        qs = super().get_queryset()
        if tenant is None:
            return qs.none()
        return qs.filter(tenant=tenant)

    def for_tenant(self, tenant=None):
        return TenantQuerySet(self.model, using=self._db).for_tenant(tenant)