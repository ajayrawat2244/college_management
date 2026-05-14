from django.http import HttpResponse

def tenants_home(request):
    return HttpResponse("Tenants Works")