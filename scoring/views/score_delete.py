from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ..models import Table


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
    is_ot_player = False
    try:
        player = table.players.get(user__username=playername)
    except Exception as e:
        print(e)
        player = table.ot_players.get(name=playername)
        is_ot_player = True

    del_records = player.delete_scores(table)
    messages.success(
        request,
        f"Deleted {del_records} records for {player} at table {table}",
    )

    if is_ot_player:
        # One-time players are deleted together with their scores.
        player.delete()
        messages.success(request, f"Deleted {player} from the table {table}.")
    else:
        # For players we need to remove the relation to the table.
        table.players.remove(player)
        messages.success(request, f"Removed {player} from the table {table}.")

    return HttpResponseRedirect(reverse("scoring:table_detail", args=[table_pk]))
