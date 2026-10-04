from django.contrib import admin

from .models import (
    Language,
    Level,
    Course,
    Lesson,
    Enrollment,
    LessonProgress,
)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "flag",
    )


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "language",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "level",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "order",
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "course",
        "enrolled_at",
    )


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "lesson",
        "completed",
        "completed_at",
    )