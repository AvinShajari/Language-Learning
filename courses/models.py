from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    flag = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name


class Level(models.Model):
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name="levels"
    )
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.language.name} - {self.name}"


class Course(models.Model):
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(
        upload_to="courses/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField()
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"],
                name="unique_user_course"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class LessonProgress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="lesson_progress"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="progress_records"
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "lesson"],
                name="unique_user_lesson"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"