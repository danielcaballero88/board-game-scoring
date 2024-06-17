from django import forms

from .models import Table


def get_scoring_form(table: Table):
    class ScoringForm(forms.Form):
        """Form to create a new score in a table."""

        name = forms.CharField(label="Player name", max_length=50)

    for sc in table.game.scoring_categories.all():
        field = forms.IntegerField(label=sc.name)
        ScoringForm.base_fields[sc.name] = field

    return ScoringForm
