from django.urls import path
from .views import tenants_home

urlpatterns = [
    path('', tenants_home, name='tenants_home'),
]