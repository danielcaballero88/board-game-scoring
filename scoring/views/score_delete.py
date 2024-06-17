from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ..models import OTPlayer, Player, Table


def get_player_or_ot_player(table: Table, playername: str):
    player = None
    try:
        player = table.players.get(user__username=playername)
    except Player.DoesNotExist:
        try:
            player = table.ot_players.get(name=playername)
        except OTPlayer.DoesNotExist:
            raise ValueError(f"Player {playername} not found in table {table}")
    return player


@require_http_methods(["POST"])
@login_required(login_url="/accounts/login")
def score_delete(
    request: HttpRequest,
    table_pk: int,
    playername: str,
):
    """Delete a player's score at a table.

    Despite the name, it needs to delete all of a players Score objects
    at a table, because each Score object is for a single scoring
    category.
    """
    table = Table.objects.get(pk=table_pk)
    # The player could be a User or an OTPlayer
    player = get_player_or_ot_player(table, playername)
    if not player.is_ot_player and player == table.owner:
        messages.error(
            request,
            f"Cannot delete scores for the owner of the table {table}.",
        )
        return HttpResponseRedirect(reverse("scoring:table_detail", args=[table_pk]))

    del_records = player.delete_scores(table)
    messages.success(
        request,
        f"Deleted {del_records} records for {player} at table {table}",
    )

    if player.is_ot_player:
        # One-time players are deleted together with their scores.
        player.delete()
        messages.success(request, f"Deleted {player} from the table {table}.")
    else:
        # For players we need to remove the relation to the table.
        table.players.remove(player)
        messages.success(request, f"Removed {player} from the table {table}.")

    return HttpResponseRedirect(reverse("scoring:table_detail", args=[table_pk]))
