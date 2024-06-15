from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from ..models import Player


@login_required(login_url="/accounts/login")
def tables_list(request: HttpRequest):
    player = Player.get_by_username(request.user.username)
    tables = player.get_tables()
    return render(
        request, "scoring/tables_list.html", {"tables": tables, "tables": tables}
    )
