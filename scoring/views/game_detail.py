from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from ..models import Game


@login_required(login_url="/accounts/login")
def game_detail(request: HttpRequest, game_pk: int):
    game = Game.objects.get(pk=game_pk)
    game_genres = ", ".join([genre.name for genre in game.genres.all()])
    context = {"game": game, "game_genres": game_genres}
    return render(request, "scoring/game_detail.html", context)
