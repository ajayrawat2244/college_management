from django.urls import path
from .views import current_tenant_settings

urlpatterns = [
    path('', current_tenant_settings, name='tenant_settings'),
]