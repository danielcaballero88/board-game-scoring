from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render


@login_required(login_url="/accounts/login")
def score_create(request: HttpRequest, table_pk: int):
    context = {"table_pk": table_pk}
    return render(request, "scoring/score_create.html", context)
