from django.http import HttpRequest
from django.shortcuts import render

from .forms import LoginForm


def login(request: HttpRequest):
    was_validated = ""

    if request.method == "GET":
        form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        is_valid = form.is_valid()
        was_validated = "was_validated"
        # If the form is valid usually the user needs to be redirected
        # to somewhere else, and if it's invalid then the default
        # response at the end should be sent so the the same page is
        # shown to the user with the same form but with the input data
        # and all validation erros.
        if is_valid:
            ...

    return render(
        request, "auth/login.html", {"form": form, "was_validated": was_validated}
    )
