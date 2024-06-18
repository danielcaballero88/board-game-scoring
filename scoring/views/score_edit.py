from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..forms import get_scoring_form
from ..models import Score, Table, get_player_or_ot_player


@login_required(login_url="/accounts/login")
def score_edit(request: HttpRequest, table_pk: int, playername: str):
    was_validated = ""

    table = Table.objects.get(pk=table_pk)
    ScoringForm = get_scoring_form(table)

    player = get_player_or_ot_player(table, playername)

    if request.method == "GET":
        # Populate form with player's scores in DB.
        scores = player.scores.filter(table=table).all()
        initial = {"name": player.name}
        for score in scores:
            initial[score.scoring_category.safe_string] = score.value
        form = ScoringForm(initial=initial)

    if request.method == "POST":
        # Add name
        updated_request = request.POST.copy()
        # If name is not in the form, add it as the player name
        if "name" not in updated_request:
            updated_request["name"] = player.name
        form = ScoringForm(updated_request)
        is_valid = form.is_valid()
        was_validated = "was_validated"
        if is_valid:
            # Update player name if it changed
            if player.name != form.cleaned_data["name"]:
                player.name = form.cleaned_data["name"]
                player.save()
                messages.info(request, f"Player name updated to {player.name}")
            # Update scores
            for sc in table.game.scoring_categories.all():
                value = form.cleaned_data[sc.safe_string]
                try:
                    score = player.scores.get(table=table, scoring_category=sc)
                    score.value = value
                    score.save()
                except Score.DoesNotExist:
                    _ = Score.objects.create(
                        table=table, player=player, scoring_category=sc, value=value
                    )
                except Exception as exc:
                    messages.error(request, f"Error updating score ({sc}): {exc}")

            messages.success(request, "Score updated successfully.")
            return HttpResponseRedirect(
                reverse("scoring:table_detail", args=[table.pk])
            )
        else:
            messages.error(request, "There was an error updating the score.")
            messages.error(request, f"Errors: {form.errors}")
            print(form.errors)

    context = {
        "table": table,
        "player": player,
        "form": form,
        "was_validated": was_validated,
    }
    return render(request, "scoring/score_edit.html", context)
