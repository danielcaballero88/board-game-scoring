from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from scoring.mocks.user import get_favorite_games, get_user_tables


@login_required(login_url="/accounts/login")
def index(request: HttpRequest):
    username = request.user.username
    previous_scores = get_user_tables(username)
    fav_games = get_favorite_games(username)

    context = {"previous_scores": previous_scores, "fav_games": fav_games}
    return render(request, "scoring/index.html", context)
