from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ..models import Game, Player


@require_http_methods(["POST"])
@login_required(login_url="/accounts/login")
def game_like(request: HttpRequest, game_pk: int):
    player = Player.get_by_username(request.user.username)
    game = Game.objects.get(pk=game_pk)
    fav_games = player.get_favorite_games()
    if game in fav_games:
        player.remove_fav_game(game)
    else:
        player.add_fav_game(game)
    return HttpResponseRedirect(reverse("scoring:games_list"))
