from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render


@login_required
def user_detail(request, user_username):
    user = User.objects.get(username=user_username)
    return render(
        request,
        'users/profile_detail.html',
        dict(
            user=user,
        ),
    )


@login_required
def edit_profile(request):
    pass


@login_required
def request_certificate(request):
    pass


@login_required
def leave(request):
    pass
