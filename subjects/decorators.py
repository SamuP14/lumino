from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from .models import Subject


def enrolled_required(function):
    def wrap(request, *args, **kwargs):
        subject_code = kwargs.get('subject_code')

        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')

        if not hasattr(request.user, 'profile'):
            return HttpResponseForbidden()

        if request.user.profile.role == 'S':
            try:
                subject = Subject.objects.get(code=subject_code)
                if subject not in request.user.students_subjects.all():
                    return HttpResponseForbidden()
            except Subject.DoesNotExist:
                return HttpResponseForbidden()

        elif request.user.profile.role == 'T':
            try:
                subject = Subject.objects.get(code=subject_code)
                if subject not in request.user.teacher_subjects.all():
                    return HttpResponseForbidden()
            except Subject.DoesNotExist:
                return HttpResponseForbidden()

        else:
            return HttpResponseForbidden()

        return function(request, *args, **kwargs)

    return wrap


def student_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')

        if not hasattr(request.user, 'profile') or request.user.profile.role != 'S':
            return HttpResponseForbidden()

        return function(request, *args, **kwargs)

    return wrap


def teacher_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')

        if not hasattr(request.user, 'profile') or request.user.profile.role != 'T':
            return HttpResponseForbidden()

        subject_code = kwargs.get('subject_code')
        subject = Subject.objects.filter(code=subject_code).first()

        if subject and subject.teacher != request.user:
            return HttpResponseForbidden()

        return function(request, *args, **kwargs)

    return wrap
