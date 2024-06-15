from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from ..models import Game


@login_required(login_url="/accounts/login")
def table_create(request: HttpRequest, game_pk: int):
    game = Game.objects.get(pk=game_pk)
    # new_table = Table(game=game, owner=request.user, start_date=timezone.now())
    new_table_url = "TBD url to send to friends"

    context = {"game": game, "new_table_url": new_table_url}

    return render(request, "scoring/table_create.html", context)
