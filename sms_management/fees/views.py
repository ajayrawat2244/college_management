from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import FeeRecord


@login_required
def fee_list(request):

    fee_records = FeeRecord.objects.filter(
        tenant=request.tenant
    )

    context = {
        "fee_records": fee_records
    }

    return render(
        request,
        "fees/list.html",
        context
    )