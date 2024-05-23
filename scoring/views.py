from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.template import loader


@login_required(login_url="/accounts/login")
def index(request: HttpRequest):
    template = loader.get_template("scoring/index.html")
    context = {}
    return render(request, "scoring/index.html", context)
