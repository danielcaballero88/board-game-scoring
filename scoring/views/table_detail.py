from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from ..models import Table


@login_required(login_url="/accounts/login")
def table_detail(request: HttpRequest, table_pk: int):
    table = Table.objects.get(pk=table_pk)
    table_players = table.players.all()
    table_players_str = ", ".join([player.user.username for player in table_players])
    # Parse scores
    table_scores_dict = table.scores_dict
    table_scores_parsed = {}
    table_scores_totals = {}
    for player, player_scores in table_scores_dict.items():
        if player not in table_scores_parsed:
            table_scores_parsed[player] = {}
            table_scores_totals[player] = 0
        for score in player_scores:
            sc = score.scoring_category
            value = score.value
            table_scores_parsed[player][sc] = value
            table_scores_totals[player] += value
    # Calculate winner
    context = {
        "table": table,
        "players": table_players_str,
        "scores": table_scores_parsed,
        "scores_totals": table_scores_totals,
        "winner": table.winner,
    }
    return render(request, "scoring/table_detail.html", context)
