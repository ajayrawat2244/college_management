from django.http import HttpResponse

def grading_home(request):
    return HttpResponse("Grading Works")