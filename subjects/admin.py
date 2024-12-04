from django.contrib import admin

from users.admin import EnrollmentinLine

from .models import Lesson, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'teacher',
    )

    inlines = [
        EnrollmentinLine,
    ]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'content',
        'subject',
    )
