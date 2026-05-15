# tenants/views.py
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

from .models import College


@login_required
def current_tenant_settings(request):
    tenant = getattr(request, "tenant", None)
    if tenant is None:
        raise Http404("Tenant not found")

    return render(request, "tenants/settings.html", {"tenant": tenant})