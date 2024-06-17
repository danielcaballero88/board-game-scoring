from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..forms import get_scoring_form
from ..models import OTPlayer, Score, Table


@login_required(login_url="/accounts/login")
def score_create_ot_player(request: HttpRequest, table_pk: int):
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
            # Create score
            name = form.cleaned_data["name"]
            # I only admit one-time players for manually created scores
            # (for now).
            # TODO: admit adding scores for registered players too.
            ot_player = OTPlayer.objects.create(name=name, table=table)
            for sc in table.game.scoring_categories.all():
                value = form.cleaned_data[sc.name]
                _ = Score.objects.create(
                    table=table, ot_player=ot_player, scoring_category=sc, value=value
                )

            messages.success(request, "Score created successfully.")
            return HttpResponseRedirect(
                reverse("scoring:table_detail", args=[table.pk])
            )
        else:
            messages.error(request, "There was an error creating the score.")
            print(form.errors)

    context = {"table": table, "form": form, "was_validated": was_validated}
    return render(request, "scoring/score_create_ot_player.html", context)
