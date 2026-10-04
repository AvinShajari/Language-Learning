from django import forms

from courses.models import Language, Level, Course, Lesson


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ["name", "code", "flag"]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "English"
            }),
            "code": forms.TextInput(attrs={
                "placeholder": "en"
            }),
            "flag": forms.TextInput(attrs={
                "placeholder": "🇬🇧"
            }),
        }


class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = ["language", "name", "description"]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "A1"
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Beginner level..."
            }),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["level", "title", "description", "image"]

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "English for Beginners"
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Course description..."
            }),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["course", "title", "description", "content", "order"]

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Introduction to English"
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Short lesson description..."
            }),
            "content": forms.Textarea(attrs={
                "placeholder": "Lesson content..."
            }),
            "order": forms.NumberInput(attrs={
                "min": 1
            }),
        }