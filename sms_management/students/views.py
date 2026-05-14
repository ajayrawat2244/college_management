from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Student

@login_required
def student_list(request):

    students = Student.objects.filter(
        tenant=request.tenant
    )

    context = {
        'students': students
    }

    return render(request, 'students/list.html', context)