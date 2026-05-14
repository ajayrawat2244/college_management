from django.utils.deprecation import MiddlewareMixin
from django.http import Http404
from django.core.cache import cache

from tenants.models import College
from core.utils import set_current_tenant


class TenantMiddleware(MiddlewareMixin):

    PUBLIC_PATHS = [
        "/admin",
        "/accounts/login",
        "/accounts/logout",
        "/static",
        "/media",
    ]

    def process_request(self, request):

        # Default tenant
        request.tenant = None

        # Clear thread-local tenant first
        set_current_tenant(None)

        host = request.get_host().split(":")[0]

        # Handle localhost development
        if host in ["127.0.0.1", "localhost"]:
            return

        parts = host.split(".")

        """
        Examples:

        college1.localhost
        college1.example.com
        """

        # Minimum subdomain requirement
        if len(parts) < 2:
            return

        subdomain = parts[0]

        # Ignore www
        if subdomain == "www":
            return

        cache_key = f"tenant:{subdomain}"

        tenant = cache.get(cache_key)

        if tenant is None:

            tenant = College.objects.filter(subdomain=subdomain).first()

            # Cache for 5 minutes
            cache.set(cache_key, tenant, 300)

        if tenant:

            request.tenant = tenant

            # Store globally
            set_current_tenant(tenant)

    def process_view(self, request, view_func, view_args, view_kwargs):

        # Allow public paths
        is_public = any(
            request.path.startswith(path)
            for path in self.PUBLIC_PATHS
        )

        if is_public:
            return None

        # Block if tenant missing
        if request.tenant is None:
            raise Http404("Tenant not found")

        return None

    def process_response(self, request, response):

        # Clear tenant after request finishes
        set_current_tenant(None)

        return response

    def process_exception(self, request, exception):

        # Cleanup on exception too
        set_current_tenant(None)

        return None