from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Language, Level, Course, Lesson

from .forms import (
    LanguageForm,
    LevelForm,
    CourseForm,
    LessonForm,
)


def staff_required(user):
    return user.is_authenticated and user.is_staff


class ManagerLoginView(LoginView):
    template_name = "dashboard/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return "/manager/"


# =========================================================
# DASHBOARD
# =========================================================

@user_passes_test(staff_required, login_url="/manager/login/")
def dashboard(request):

    context = {
        "languages_count": Language.objects.count(),
        "levels_count": Level.objects.count(),
        "courses_count": Course.objects.count(),
        "lessons_count": Lesson.objects.count(),
        "recent_courses": Course.objects.order_by("-id")[:5],
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


# =========================================================
# LANGUAGES
# =========================================================

@user_passes_test(staff_required, login_url="/manager/login/")
def language_list(request):

    languages = Language.objects.all()

    return render(
        request,
        "dashboard/languages.html",
        {
            "languages": languages
        }
    )


@user_passes_test(staff_required, login_url="/manager/login/")
def language_create(request):

    if request.method == "POST":

        form = LanguageForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("language_list")

    else:
        form = LanguageForm()

    return render(
        request,
        "dashboard/language_form.html",
        {
            "form": form,
            "title": "Add Language"
        }
    )


@user_passes_test(staff_required, login_url="/manager/login/")
def language_edit(request, pk):

    language = get_object_or_404(Language, pk=pk)

    if request.method == "POST":

        form = LanguageForm(
            request.POST,
            instance=language
        )

        if form.is_valid():
            form.save()
            return redirect("language_list")

    else:

        form = LanguageForm(
            instance=language
        )

    return render(
        request,
        "dashboard/language_form.html",
        {
            "form": form,
            "title": "Edit Language"
        }
    )


@user_passes_test(staff_required, login_url="/manager/login/")
def language_delete(request, pk):

    language = get_object_or_404(
        Language,
        pk=pk
    )

    if request.method == "POST":

        language.delete()

        return redirect("language_list")

    return render(
        request,
        "dashboard/language_delete.html",
        {
            "language": language
        }
    )


# =========================================================
# LEVELS
# =========================================================

@user_passes_test(staff_required, login_url="/manager/login/")
def level_list(request):

    levels = Level.objects.select_related(
        "language"
    ).all()

    return render(
        request,
        "dashboard/levels.html",
        {
            "levels": levels
        }
    )


@user_passes_test(staff_required, login_url="/manager/login/")
def level_create(request):

    if request.method == "POST":

        form = LevelForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("level_list")

    else:
        form = LevelForm()

    return render(
        request,
        "dashboard/level_form.html",
        {
            "form": form,
            "title": "Add Level"
        }
    )


@user_passes_test(staff_required, login_url="/manager/login/")
def level_edit(request, pk):

    level = get_object_or_404(
        Level,
        pk=pk
    )

    if request.method == "POST":

        form = LevelForm(
            request.POST,
            instance=level
        )

        if form.is_valid():
            form.save()
            return redirect("level_list")

    else:

        form = LevelForm(
            instance=level
        )

    return render(
        request,
        "dashboard/level_form.html",
        {
            "form": form,
            "title": "Edit Level"
        }
    )


@user_passes_test(staff_required, login_url="/manager/login/")
def level_delete(request, pk):

    level = get_object_or_404(
        Level,
        pk=pk
    )

    if request.method == "POST":

        level.delete()

        return redirect("level_list")

    return render(
        request,
        "dashboard/level_delete.html",
        {
            "level": level
        }
    )


# =========================================================
# COURSES
# =========================================================

@user_passes_test(staff_required, login_url="/manager/login/")
def course_list(request):

    courses = Course.objects.select_related(
        "level",
        "level__language"
    ).all()

    return render(
        request,
        "dashboard/courses.html",
        {
            "courses": courses
        }
    )


@user_passes_test(staff_required, login_url="/manager/login/")
def course_create(request):

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect("course_list")

    else:

        form = CourseForm()

    return render(
        request,
        "dashboard/course_form.html",
        {
            "form": form,
            "title": "Add Course"
        }
    )


@user_passes_test(staff_required, login_url="/manager/login/")
def course_edit(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            request.FILES,
            instance=course
        )

        if form.is_valid():
            form.save()
            return redirect("course_list")

    else:

        form = CourseForm(
            instance=course
        )

    return render(
        request,
        "dashboard/course_form.html",
        {
            "form": form,
            "title": "Edit Course"
        }
    )


@user_passes_test(staff_required, login_url="/manager/login/")
def course_delete(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == "POST":

        course.delete()

        return redirect("course_list")

    return render(
        request,
        "dashboard/course_delete.html",
        {
            "course": course
        }
    )


# =========================================================
# LESSONS
# =========================================================

@user_passes_test(staff_required, login_url="/manager/login/")
def lesson_list(request):

    lessons = Lesson.objects.select_related(
        "course",
        "course__level",
        "course__level__language"
    ).all()

    return render(
        request,
        "dashboard/lessons.html",
        {
            "lessons": lessons
        }
    )


@user_passes_test(staff_required, login_url="/manager/login/")
def lesson_create(request):

    if request.method == "POST":

        form = LessonForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("lesson_list")

    else:

        form = LessonForm()

    return render(
        request,
        "dashboard/lesson_form.html",
        {
            "form": form,
            "title": "Add Lesson"
        }
    )


@user_passes_test(staff_required, login_url="/manager/login/")
def lesson_edit(request, pk):

    lesson = get_object_or_404(
        Lesson,
        pk=pk
    )

    if request.method == "POST":

        form = LessonForm(
            request.POST,
            instance=lesson
        )

        if form.is_valid():
            form.save()
            return redirect("lesson_list")

    else:

        form = LessonForm(
            instance=lesson
        )

    return render(
        request,
        "dashboard/lesson_form.html",
        {
            "form": form,
            "title": "Edit Lesson"
        }
    )


@user_passes_test(staff_required, login_url="/manager/login/")
def language_delete(request, pk):
    language = get_object_or_404(Language, pk=pk)
    language.delete()
    return redirect("language_list")


@user_passes_test(staff_required, login_url="/manager/login/")
def level_delete(request, pk):
    level = get_object_or_404(Level, pk=pk)
    level.delete()
    return redirect("level_list")


@user_passes_test(staff_required, login_url="/manager/login/")
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect("course_list")


@user_passes_test(staff_required, login_url="/manager/login/")
def lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    lesson.delete()
    return redirect("lesson_list")