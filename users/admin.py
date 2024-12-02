from django.contrib import admin

from .models import Enrollment, Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'role',
        'bio',
        'avatar',
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    pass
