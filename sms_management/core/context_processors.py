from core.utils import get_current_tenant


def tenant_context(request):
    return {
        "current_tenant": getattr(request, "tenant", None) or get_current_tenant()
    }