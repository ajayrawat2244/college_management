from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import Student


@login_required
def student_list(request):
    students = (Student.all_objects.select_related("user", "tenant").filter(tenant=request.tenant).order_by("-enrollment_date"))
    return render(request, "students/list.html", {"students": students})


@login_required
def student_detail(request, pk):
    if request.tenant is None:
        raise Http404("Tenant not found")

    student = get_object_or_404(
        Student.all_objects.select_related("user", "tenant"),
        pk=pk,
        tenant=request.tenant,
    )

    wallet = getattr(student, "wallet", None)
    fee_record = getattr(student, "fee_record", None)

    return render(
        request,
        "students/detail.html",
        {
            "student": student,
            "wallet_balance": getattr(wallet, "balance", 0),
            "pending_amount": getattr(fee_record, "pending_amount", 0),
        },
    )