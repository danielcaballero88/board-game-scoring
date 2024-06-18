from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..forms import get_scoring_form
from ..models import OTPlayer, Player, Score, Table


def score_create_self(request: HttpRequest, table_pk: int):
    was_validated = ""

    table = Table.objects.get(pk=table_pk)
    ScoringForm = get_scoring_form(table)

    if request.method == "GET":
        form = ScoringForm()

    if request.method == "POST":
        form = ScoringForm(request.POST)
        is_valid = form.is_valid()
        was_validated = "was_validated"
        if is_valid:
            # The flow is different for authenticated users and for
            # anonymous users (one-time players).
            if request.user.is_authenticated:
                player = Player.objects.get(user=request.user)
            else:
                name = form.cleaned_data["name"]
                player = OTPlayer.objects.create(name=name, table=table)

            for sc in table.game.scoring_categories.all():
                value = form.cleaned_data[sc.safe_string]
                score_dict = {
                    "table": table,
                    "scoring_category": sc,
                    "value": value,
                }
                if request.user.is_authenticated:
                    score_dict["player"] = player
                else:
                    score_dict["ot_player"] = player

                _ = Score.objects.create(**score_dict)

            messages.success(request, "Score created successfully.")
            if request.user.is_authenticated:
                return HttpResponseRedirect(
                    reverse("scoring:table_detail", args=[table.pk])
                )
            else:
                return render(
                    request,
                    "scoring/score_create_self_success.html",
                    {"table": table, "player": player},
                )
        else:
            messages.error(request, "There was an error creating the score.")
            print(form.errors)

    context = {"table": table, "form": form, "was_validated": was_validated}
    return render(request, "scoring/score_create_self.html", context)
