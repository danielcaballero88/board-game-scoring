from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("scoring:index")

    was_validated = ""

    if request.method == "GET":
        if "next" in request.GET:
            request.session["next"] = request.GET["next"]
        else:
            request.session["next"] = reverse("scoring:index")
        form = LoginForm()

    if request.method == "POST":
        next = request.session.get("next", reverse("scoring:index"))
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
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                # No backend authenticated the credentials
                form.add_error(None, "Wrong credentials")

    return render(
        request, "auth/login.html", {"form": form, "was_validated": was_validated}
    )


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("/")
