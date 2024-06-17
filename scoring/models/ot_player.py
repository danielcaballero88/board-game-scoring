from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from .table import Table

if TYPE_CHECKING:
    from .score import Score


class OTPlayer(models.Model):
    """Model representing a one-time player.

    A one time player is a player that is not registered in the system.
    It is invited at a table to enter their score so it can be included
    in the scoring, but they don't yet have an account and they can't
    create tables of their own.

    Attributes:
        - name: A unique per table name (cannot be the same as other
        one time player not the same as a username of a player invited).
    Relationships:
        - table (many to one): The table that the player is invited to.
        - scores (one to many): The scores for this one-time player.
    """

    name = models.CharField(max_length=50)
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name="ot_players"
    )
    is_ot_player = True

    class Meta:
        # Each one-time player should have a unique name in the table.
        constraints = [
            models.UniqueConstraint(
                name="unique_ot_player_name_per_table",
                fields=["name", "table"],
            )
        ]

    def get_scores_by_table(self, _table: Table) -> list[Score]:
        """Method to mimic the one in Player.

        Here the table is not used because each OTPlayer is associated
        with a single table.
        """
        return self.scores.all()

    def delete_scores(self, table: Table) -> int:
        """Delete all scores for this player at a table.

        The table arg is not needed but it's present to mimic the method
        in Player. Besides deleting the scores, it should also delete
        the OTPlayer object itself.
        """
        return self.scores.all().delete()

    def __str__(self):
        return f"{self.name} at {self.table}"
