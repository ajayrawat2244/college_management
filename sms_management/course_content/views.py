from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from academics.models import Course
from course_content.models import CourseContent, ContentReview, LiveClass
from students.models import Student


@login_required
def course_content_list(request, course_id):
    course = get_object_or_404(Course, id=course_id, tenant=request.tenant)
    contents = CourseContent.objects.filter(
        tenant=request.tenant,
        course=course,
        is_published=True
    ).order_by("order", "created_at")

    return render(request, "course_content/list.html", {
        "course": course,
        "contents": contents,
    })


@login_required
def course_content_detail(request, content_id):
    content = get_object_or_404(CourseContent, id=content_id, tenant=request.tenant)

    reviews = content.reviews.select_related("student").all()

    return render(request, "course_content/detail.html", {
        "content": content,
        "reviews": reviews,
    })


@login_required
def add_review(request, content_id):
    content = get_object_or_404(CourseContent, id=content_id, tenant=request.tenant)

    student = get_object_or_404(Student, user=request.user, tenant=request.tenant)

    if request.method == "POST":
        rating = int(request.POST.get("rating", 0))
        review_text = request.POST.get("review", "").strip()

        review, created = ContentReview.objects.update_or_create(
            tenant=request.tenant,
            content=content,
            student=student,
            defaults={
                "rating": rating,
                "review": review_text,
            }
        )

        messages.success(request, "Review saved successfully.")
        return redirect("course_content_detail", content_id=content.id)

    return render(request, "course_content/review_form.html", {
        "content": content
    })


@login_required
def live_class_list(request, course_id):
    course = get_object_or_404(Course, id=course_id, tenant=request.tenant)

    live_classes = LiveClass.objects.filter(
        tenant=request.tenant,
        course=course
    ).order_by("starts_at")

    return render(request, "course_content/live_class_list.html", {
        "course": course,
        "live_classes": live_classes,
    })


@login_required
def live_class_detail(request, live_class_id):
    live_class = get_object_or_404(LiveClass, id=live_class_id, tenant=request.tenant)

    return render(request, "course_content/live_class_detail.html", {
        "live_class": live_class,
        "is_expired": live_class.starts_at <= timezone.now(),
    })


@login_required
def join_live_class(request, live_class_id):
    live_class = get_object_or_404(LiveClass, id=live_class_id, tenant=request.tenant)

    if live_class.starts_at <= timezone.now():
        messages.error(request, "This live class has already started or passed.")
        return redirect("live_class_detail", live_class_id=live_class.id)

    return redirect(live_class.meeting_url)