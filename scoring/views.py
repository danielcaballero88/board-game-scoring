from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Game, Player, Table


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


@login_required(login_url="/accounts/login")
def games_list(request: HttpRequest):
    games = Game.objects.all()
    player = Player.get_by_username(request.user.username)
    fav_games = player.get_favorite_games()
    for game in games:
        if game in fav_games:
            game.is_favorite = True
    return render(request, "scoring/games_list.html", {"games": games})


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


@login_required(login_url="/accounts/login")
def tables_list(request: HttpRequest):
    player = Player.get_by_username(request.user.username)
    tables = player.get_tables()
    return render(
        request, "scoring/tables_list.html", {"tables": tables, "tables": tables}
    )


@login_required(login_url="/accounts/login")
def table_create(request: HttpRequest, game_pk: int):
    game = Game.objects.get(pk=game_pk)
    # new_table = Table(game=game, owner=request.user, start_date=timezone.now())
    new_table_url = "TBD url to send to friends"

    context = {"game": game, "new_table_url": new_table_url}

    return render(request, "scoring/table_create.html", context)


@login_required(login_url="/accounts/login")
def game_detail(request: HttpRequest, game_pk: int):
    game = Game.objects.get(pk=game_pk)
    game_genres = ", ".join([genre.name for genre in game.genres.all()])
    context = {"game": game, "game_genres": game_genres}
    return render(request, "scoring/game_detail.html", context)


@login_required(login_url="/accounts/login")
def table_detail(request: HttpRequest, table_pk: int):
    table = Table.objects.get(pk=table_pk)
    table_players = ", ".join([player.user.username for player in table.players.all()])
    context = {"table": table, "table_players": table_players}
    return render(request, "scoring/table_detail.html", context)
