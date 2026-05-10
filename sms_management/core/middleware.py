from django.utils.deprecation import MiddlewareMixin
from tenants.models import College
from core.utils import set_current_tenant


class TenantMiddleware(MiddlewareMixin):

    def process_request(self, request):

        host = request.get_host().split(":")[0]
        parts = host.split(".")

        if len(parts) < 3:
            request.tenant = None
            return

        subdomain = parts[0]

        try:
            tenant = College.objects.get(subdomain=subdomain)

            request.tenant = tenant

            # store globally
            set_current_tenant(tenant)

        except College.DoesNotExist:
            request.tenant = None