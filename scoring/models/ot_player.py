from django.db import models


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
    """

    name = models.CharField(max_length=50)
    table = models.ForeignKey(
        "Table", on_delete=models.CASCADE, related_name="ot_players"
    )

    class Meta:
        # Each one-time player should have a unique name in the table.
        constraints = [
            models.UniqueConstraint(
                name="unique_ot_player_name_per_table",
                fields=["name", "table"],
            )
        ]

    def __str__(self):
        return f"{self.name} at {self.table}"
