from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from ..models import Player


@login_required(login_url="/accounts/login")
def index(request: HttpRequest):
    username = request.user.username
    player = Player.get_by_username(username)
    previous_scores = player.get_tables()
    fav_games = player.get_favorite_games()
    # Attach the record (won/played count) for each favorite game to
    # each game object so it is available in the template.
    for fav_game in fav_games:
        fav_game.record = player.get_record(fav_game)

    context = {
        "previous_scores": previous_scores,
        "fav_games": fav_games,
    }
    return render(request, "scoring/index.html", context)
