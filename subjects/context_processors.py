from .models import Subject


def user_subjects(request):
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)

        if profile:
            if profile.is_student():
                enrolled_subjects = request.user.enrolled.all().values_list('subject', flat=True)
                subjects = Subject.objects.filter(pk__in=enrolled_subjects)
            elif profile.role == profile.Role.TEACHER:
                subjects = Subject.objects.filter(teacher=request.user)
            else:
                subjects = Subject.objects.none()
        else:
            subjects = Subject.objects.none()
    else:
        subjects = Subject.objects.none()

    return {'subjects': subjects}
