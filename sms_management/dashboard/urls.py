from django.urls import path
from .views import dashboard_view, TenantDashboardAPIView

urlpatterns = [
    path("api/dashboard/", TenantDashboardAPIView.as_view(), name="tenant_dashboard_api"),
    path("", dashboard_view, name="dashboard_view"),
]