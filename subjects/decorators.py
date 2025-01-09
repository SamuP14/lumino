from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def student_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')

        if not hasattr(request.user, 'profile'):
            if request.user.profile.role != 'S':
                return HttpResponseForbidden()

        return function(request, *args, **kwargs)

    return wrap


def teacher_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')

        if not hasattr(request.user, 'profile'):
            if request.user.profile.role != 'T':
                return HttpResponseForbidden()

        return function(request, *args, **kwargs)

    return wrap
