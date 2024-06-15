from typing import cast

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from ..models import Score, Table


@login_required(login_url="/accounts/login")
def table_detail(request: HttpRequest, table_pk: int):
    table = Table.objects.get(pk=table_pk)
    table_players = table.players.all()
    table_players_str = ", ".join([player.user.username for player in table_players])
    # Parse scores
    table_scores = cast(list[Score], table.scores.all())
    table_scores_parsed = {}
    table_scores_totals = {}
    for table_score in table_scores:
        username = table_score.get_player_name()
        category = table_score.scoring_category.name
        value = table_score.value
        if username not in table_scores_parsed:
            table_scores_parsed[username] = {}
            table_scores_totals[username] = 0
        table_scores_parsed[username][category] = value
        table_scores_totals[username] += value
    # Calculate winner
    winner = max(table_scores_totals, key=table_scores_totals.get)

    context = {
        "table": table,
        "players": table_players_str,
        "scores": table_scores_parsed,
        "scores_totals": table_scores_totals,
        "winner": winner,
    }
    return render(request, "scoring/table_detail.html", context)
