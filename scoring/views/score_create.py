from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from ..models import Table


@login_required(login_url="/accounts/login")
def score_create(request: HttpRequest, table_pk: int):
    table = Table.objects.get(pk=table_pk)
    context = {"table": table}
    return render(request, "scoring/score_create.html", context)
