from django.urls import path
from .views import TenantDashboardAPIView

urlpatterns = [
    path("api/dashboard/", TenantDashboardAPIView.as_view(), name="tenant_dashboard_api"),
]