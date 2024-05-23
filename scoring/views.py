from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render


@login_required(login_url="/accounts/login")
def index(request: HttpRequest):
    context = {}
    return render(request, "scoring/index.html", context)
