from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from shared.decorators import student_required

from .forms import EditProfileForm


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
    user = User.objects.get(username=request.user.username)
    profile = user.profile

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'User profile has been successfully saved.')
            return redirect(profile)
        else:
            messages.error(request, 'Error updating the profile. Please check the form.')

    else:
        form = EditProfileForm(instance=profile)

    return render(
        request,
        'users/edit_profile.html',
        {'form': form, 'profile': profile},
    )


@student_required
@login_required
def leave(request):
    user = request.user
    user.delete()
    messages.success(request, 'Good bye! Hope to see you soon.')

    return redirect('/')
