from django.db.models import Sum, Count
from django.db.models.functions import Coalesce

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required

from students.models import Student, Enquiry
from fees.models import FeeRecord
from django.shortcuts import render



def dashboard_context(tenant):
    recent_students = Student.objects.filter(tenant=tenant).select_related("user").order_by("-enrollment_date")[:5]
    return {
        "tenant": tenant,
        "total_admissions": Student.objects.filter(tenant=tenant).count(),
        "total_enquiries": Enquiry.objects.filter(tenant=tenant).count(),
        "total_revenue": FeeRecord.objects.filter(tenant=tenant).aggregate(total=Coalesce(Sum("paid_amount"), 0))["total"],
        "recent_students": recent_students,
    }

@login_required
def dashboard_view(request):
    return render(request, "dashboard/dashboard.html", dashboard_context(request.tenant))


class TenantDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tenant = request.tenant
        total_admissions = Student.objects.filter(tenant=tenant).count()

        # Temporary because enquiry model doesn't exist yet
        total_enquiries = 0
        total_revenue = FeeRecord.objects.filter(
            tenant=tenant
        ).aggregate(
            total=Coalesce(Sum("paid_amount"), 0)
        )["total"]

        total_enquiries = Enquiry.objects.filter(tenant=tenant).count()

        return Response({
            "tenant": tenant.name,
            "total_admissions": total_admissions,
            "total_enquiries": total_enquiries,
            "total_revenue": total_revenue,
        })