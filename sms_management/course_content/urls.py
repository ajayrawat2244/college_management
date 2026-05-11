from django.urls import path
from . import views

urlpatterns = [
    path("course/<int:course_id>/contents/", views.course_content_list, name="course_content_list"),
    path("content/<int:content_id>/", views.course_content_detail, name="course_content_detail"),
    path("content/<int:content_id>/review/", views.add_review, name="add_review"),
    path("course/<int:course_id>/live-classes/", views.live_class_list, name="live_class_list"),
    path("live-class/<int:live_class_id>/", views.live_class_detail, name="live_class_detail"),
    path("live-class/<int:live_class_id>/join/", views.join_live_class, name="join_live_class"),
]