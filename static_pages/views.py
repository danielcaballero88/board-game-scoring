from django.http import HttpRequest
from django.shortcuts import render


def landing(request: HttpRequest):
    context = {}
    return render(request, "static_pages/landing.html", context)
