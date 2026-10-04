import json
import os

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from openai import OpenAI

from .forms import SignUpForm
from .models import (
    Language,
    Level,
    Course,
    Lesson,
    Enrollment,
    LessonProgress,
)


def home(request):
    languages = Language.objects.all()

    courses = Course.objects.select_related(
        "level",
        "level__language"
    ).all()[:6]

    return render(
        request,
        "courses/home.html",
        {
            "languages": languages,
            "courses": courses,
        }
    )


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Your account has been created successfully."
            )

            return redirect("home")

    else:
        form = SignUpForm()

    return render(
        request,
        "courses/signup.html",
        {
            "form": form
        }
    )


def language_detail(request, pk):
    language = get_object_or_404(Language, pk=pk)

    levels = language.levels.prefetch_related(
        "courses"
    ).all()

    return render(
        request,
        "courses/language_detail.html",
        {
            "language": language,
            "levels": levels,
        }
    )


def course_detail(request, pk):
    course = get_object_or_404(
        Course.objects.select_related(
            "level",
            "level__language"
        ).prefetch_related("lessons"),
        pk=pk
    )

    enrolled = False

    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(
            user=request.user,
            course=course
        ).exists()

    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course,
            "enrolled": enrolled,
        }
    )


@login_required(login_url="/login/")
def enroll_course(request, pk):
    course = get_object_or_404(
        Course,
        pk=pk
    )

    Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    return redirect(
        "course_detail",
        pk=course.pk
    )


@login_required(login_url="/login/")
def lesson_detail(request, pk):
    lesson = get_object_or_404(
        Lesson.objects.select_related(
            "course",
            "course__level",
            "course__level__language"
        ),
        pk=pk
    )

    enrollment = Enrollment.objects.filter(
        user=request.user,
        course=lesson.course
    ).exists()

    if not enrollment:
        return redirect(
            "course_detail",
            pk=lesson.course.pk
        )

    progress, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )

    lessons = list(
        lesson.course.lessons.all()
    )

    current_index = lessons.index(lesson)

    previous_lesson = (
        lessons[current_index - 1]
        if current_index > 0
        else None
    )

    next_lesson = (
        lessons[current_index + 1]
        if current_index < len(lessons) - 1
        else None
    )

    return render(
        request,
        "courses/lesson_detail.html",
        {
            "lesson": lesson,
            "progress": progress,
            "previous_lesson": previous_lesson,
            "next_lesson": next_lesson,
        }
    )


@login_required(login_url="/login/")
def complete_lesson(request, pk):
    lesson = get_object_or_404(
        Lesson,
        pk=pk
    )

    progress, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )

    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()

    return redirect(
        "lesson_detail",
        pk=lesson.pk
    )


@login_required(login_url="/login/")
def my_courses(request):
    enrollments = Enrollment.objects.filter(
        user=request.user
    ).select_related(
        "course",
        "course__level",
        "course__level__language"
    )

    return render(
        request,
        "courses/my_courses.html",
        {
            "enrollments": enrollments
        }
    )


@login_required(login_url="/login/")
def ai_tutor(request):

    if request.method == "GET":
        return render(
            request,
            "courses/ai_tutor.html"
        )

    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed."},
            status=405
        )

    try:
        data = json.loads(request.body)

        message = data.get(
            "message",
            ""
        ).strip()

        if not message:
            return JsonResponse(
                {
                    "error": "Please enter a message."
                },
                status=400
            )

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if not api_key:
            return JsonResponse(
                {
                    "error": "OpenAI API key is not configured."
                },
                status=500
            )

        client = OpenAI(
            api_key=api_key
        )

        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions="""
You are Lingua AI Tutor, an expert English language teacher.

Your job is to actually teach the learner.

Rules:

- Adapt explanations to the learner's level.
- Correct mistakes gently.
- Show the corrected sentence.
- Explain why the correction is necessary.
- Give practical everyday examples.
- Help with vocabulary, grammar, speaking,
  writing, reading and listening.
- Ask short practice questions when useful.
- Encourage the learner to continue practicing.
- Keep explanations clear and reasonably concise.
- If the learner asks for a lesson,
  create a structured mini lesson.
- If the learner writes incorrect English,
  correct it and explain the mistake.
- Never shame the learner.

The student should actively produce English
rather than only reading explanations.
""",
            input=message
        )

        return JsonResponse(
            {
                "reply": response.output_text
            }
        )

    except Exception as e:

        print(
            "AI TUTOR ERROR:",
            repr(e)
        )

        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )