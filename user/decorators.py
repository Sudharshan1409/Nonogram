from django.shortcuts import HttpResponseRedirect, redirect
from django.contrib import messages
from django.urls import reverse


def should_not_be_logged_in(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('home')
        else:
            return func(request, *args, **kwargs)
    return wrapper_func


def super_user_or_not(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return func(request, *args, **kwargs)
            else:
                messages.warning(request, 'You are not allowed to access this page')
                return redirect('home')
        else:
            messages.warning(request, 'You have to login first to access this page')
            return redirect('user:login')
    return wrapper_func
