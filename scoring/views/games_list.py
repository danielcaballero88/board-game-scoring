from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from ..models import Game, Player


@login_required(login_url="/accounts/login")
def games_list(request: HttpRequest):
    games = Game.objects.all()
    player = Player.get_by_username(request.user.username)
    fav_games = player.get_favorite_games()
    for game in games:
        if game in fav_games:
            game.is_favorite = True
    return render(request, "scoring/games_list.html", {"games": games})
