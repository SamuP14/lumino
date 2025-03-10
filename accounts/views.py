from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, SignupForm


def user_login(request):
    FALLBACK_REDIRECT = reverse('index')
    if request.user.is_authenticated:
        return redirect(FALLBACK_REDIRECT)
    if request.method == 'POST':
        if (form := LoginForm(request.POST)).is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if user := authenticate(request, username=username, password=password):
                login(request, user)
                messages.add_message(request, messages.INFO, 'Welcome to Lumino. Nice to see you!')

                return redirect(request.GET.get('next', FALLBACK_REDIRECT))
            else:
                form.add_error(None, 'Incorrect username or password.')
    else:
        form = LoginForm()
    return render(
        request,
        'accounts/login.html',
        dict(form=form),
    )


def user_logout(request):
    logout(request)
    return redirect('index')


def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.add_message(request, messages.INFO, 'Welcome to Lumino. Nice to see you!')
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', dict(form=form))
