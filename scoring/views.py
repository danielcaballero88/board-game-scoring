from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render


@login_required(login_url="/accounts/login")
def landing(request: HttpRequest):
    context = {}
    return render(request, "scoring/landing.html", context)
