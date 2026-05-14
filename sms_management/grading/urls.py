from django.urls import path
from .views import grading_home

urlpatterns = [
    path('', grading_home, name='grading_home'),
]