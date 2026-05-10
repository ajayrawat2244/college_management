from django.shortcuts import render
from .models import Student

def student_list(request):

    students = Student.objects.for_tenant(request.tenant)

    return render(request, "students/list.html", {
        "students": students
    })