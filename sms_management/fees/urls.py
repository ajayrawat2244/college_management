from django.urls import path
from .views import fee_list

urlpatterns = [
    path('', fee_list, name='fee_list'),

]