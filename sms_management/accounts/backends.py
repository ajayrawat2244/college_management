from django.contrib.auth.backends import BaseBackend
from accounts.models import User

class TenantAuthenticationBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        if request is None:
            return None

        tenant = getattr(request, "tenant", None)

        try:
            if tenant:
                user = User.objects.get(
                    email=username,
                    tenant=tenant
                )
            else:
                # fallback for superadmin/admin login
                user = User.objects.get(
                    email=username,
                    is_superuser=True
                )

        except User.DoesNotExist:
            return None

        except User.MultipleObjectsReturned:
            return None

        if user.check_password(password) and user.is_active:
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None