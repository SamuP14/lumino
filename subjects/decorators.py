from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from .models import Subject


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
