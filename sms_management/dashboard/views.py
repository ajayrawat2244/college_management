from django.db.models import Sum
from django.db.models.functions import Coalesce

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from students.models import Student, Enquiry
from fees.models import FeeRecord


class TenantDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        tenant = request.tenant

        total_admissions = Student.objects.filter(
            tenant=tenant
        ).count()

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