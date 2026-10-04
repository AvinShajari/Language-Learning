from django.urls import path

from .views import (
    home,
    signup,
    language_detail,
    course_detail,
    enroll_course,
    lesson_detail,
    complete_lesson,
    my_courses,
    ai_tutor,
)


urlpatterns = [

    path(
        "",
        home,
        name="home"
    ),

    path(
        "signup/",
        signup,
        name="signup"
    ),

    path(
        "languages/<int:pk>/",
        language_detail,
        name="language_detail"
    ),

    path(
        "courses/<int:pk>/",
        course_detail,
        name="course_detail"
    ),

    path(
        "courses/<int:pk>/enroll/",
        enroll_course,
        name="enroll_course"
    ),

    path(
        "lessons/<int:pk>/",
        lesson_detail,
        name="lesson_detail"
    ),

    path(
        "lessons/<int:pk>/complete/",
        complete_lesson,
        name="complete_lesson"
    ),

    path(
        "my-courses/",
        my_courses,
        name="my_courses"
    ),

    path(
        "ai-tutor/",
        ai_tutor,
        name="ai_tutor"
    ),
]