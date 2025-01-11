from .models import Subject


def user_subjects(request):
    if request.user.is_authenticated:
        # Obtener el perfil del usuario
        profile = getattr(request.user, 'profile', None)

        if profile:
            if profile.is_student():  # Si es estudiante, mostrar asignaturas matriculadas
                enrolled_subjects = request.user.enrolled.all().values_list('subject', flat=True)
                subjects = Subject.objects.filter(pk__in=enrolled_subjects)
            elif (
                profile.role == profile.Role.TEACHER
            ):  # Si es profesor, mostrar asignaturas que imparte
                subjects = Subject.objects.filter(teacher=request.user)
            else:
                subjects = (
                    Subject.objects.none()
                )  # No mostrar asignaturas si no es estudiante ni profesor
        else:
            subjects = Subject.objects.none()  # Si no hay perfil, no mostrar asignaturas
    else:
        subjects = Subject.objects.none()  # Si no está autenticado, no mostrar asignaturas

    return {'subjects': subjects}
