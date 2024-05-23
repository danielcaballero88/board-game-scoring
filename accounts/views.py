from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.http import HttpRequest
from django.shortcuts import render

from .forms import LoginForm
from .utils import get_user_by_email


def login(request: HttpRequest):
    was_validated = ""

    if request.method == "GET":
        form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        is_valid = form.is_valid()
        was_validated = "was_validated"
        if is_valid:
            # Get user data.
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            # Authenticate and login
            user = authenticate(email=email, password=password)
            if user is not None:
                # A backend authenticated the credentials
                django_login(request, user)
                messages.success(request, f"Login success for {email}:{password}")
            else:
                # No backend authenticated the credentials
                form.add_error(None, "Wrong credentials")
            # redirect to a new URL:
            # (commented out for now because the login page is the only page so far)
            # return HttpResponseRedirect(reverse("<app>:<url>"))

    return render(
        request, "auth/login.html", {"form": form, "was_validated": was_validated}
    )
