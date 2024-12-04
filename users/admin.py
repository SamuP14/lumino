from django.contrib import admin

from subjects.models import Enrollment

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'role',
        'bio',
        'avatar',
    )


class EnrollmentinLine(admin.TabularInline):
    model = Enrollment
    extra = 1
