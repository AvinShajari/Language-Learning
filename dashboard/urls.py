from django.urls import path

from .views import (
    ManagerLoginView,
    dashboard,

    language_list,
    language_create,
    language_edit,
    language_delete,

    level_list,
    level_create,
    level_edit,
    level_delete,

    course_list,
    course_create,
    course_edit,
    course_delete,

    lesson_list,
    lesson_create,
    lesson_edit,
    lesson_delete,
)


urlpatterns = [

    # Login
    path(
        "login/",
        ManagerLoginView.as_view(),
        name="manager_login"
    ),

    # Dashboard
    path(
        "",
        dashboard,
        name="dashboard"
    ),

    # Languages
    path(
        "languages/",
        language_list,
        name="language_list"
    ),

    path(
        "languages/add/",
        language_create,
        name="language_create"
    ),

    path(
        "languages/<int:pk>/edit/",
        language_edit,
        name="language_edit"
    ),

    path(
        "languages/<int:pk>/delete/",
        language_delete,
        name="language_delete"
    ),

    # Levels
    path(
        "levels/",
        level_list,
        name="level_list"
    ),

    path(
        "levels/add/",
        level_create,
        name="level_create"
    ),

    path(
        "levels/<int:pk>/edit/",
        level_edit,
        name="level_edit"
    ),

    path(
        "levels/<int:pk>/delete/",
        level_delete,
        name="level_delete"
    ),

    # Courses
    path(
        "courses/",
        course_list,
        name="course_list"
    ),

    path(
        "courses/add/",
        course_create,
        name="course_create"
    ),

    path(
        "courses/<int:pk>/edit/",
        course_edit,
        name="course_edit"
    ),

    path(
        "courses/<int:pk>/delete/",
        course_delete,
        name="course_delete"
    ),

    # Lessons
    path(
        "lessons/",
        lesson_list,
        name="lesson_list"
    ),

    path(
        "lessons/add/",
        lesson_create,
        name="lesson_create"
    ),

    path(
        "lessons/<int:pk>/edit/",
        lesson_edit,
        name="lesson_edit"
    ),

    path(
        "lessons/<int:pk>/delete/",
        lesson_delete,
        name="lesson_delete"
    ),
]