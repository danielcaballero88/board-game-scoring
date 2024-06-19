from django import forms

from .models import Table


def get_scoring_form(table: Table):
    class ScoringForm(forms.Form):
        """Form to create a new score in a table."""

        name = forms.CharField(max_length=50)

        # Add validation for `name` field to prevent duplicate names
        # in the same table.
        def clean_name(self):
            name = self.cleaned_data["name"]
            if (
                table.ot_players.filter(name=name).exists()
                or table.players.filter(user__username=name).exists()
            ):
                raise forms.ValidationError("Name already exists in this table.")
            return name

    for sc in table.game.scoring_categories.all():
        field = forms.IntegerField(label=sc.name)
        ScoringForm.base_fields[sc.safe_string] = field

    return ScoringForm
