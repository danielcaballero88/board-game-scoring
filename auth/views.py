from django.shortcuts import render
from django.http import HttpRequest

from .forms import LoginForm


def login(request: HttpRequest):
    if request.method == "GET":
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})
