from django.db import models

from .player import Player
from .scoring_category import ScoringCategory
from .table import Table


class Score(models.Model):
    """Model representing a score for a player, table, scoring category.

    Attributes:
        - value: The value of the score.
    Relationships:
        - player (many to one)
        - scoring_category (many to one)
        - table (many to one)

    Validation:
        - It's important to check that the scoring category belongs to
        the game that the table is for.
    """

    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="scores")
    player = models.ForeignKey(Player, on_delete=models.PROTECT, related_name="scores")
    scoring_category = models.ForeignKey(
        ScoringCategory, on_delete=models.PROTECT, related_name="scores"
    )
    value = models.IntegerField()

    class Meta:
        # Each player can only have one score for each scoring category
        # in a table.
        constraints = [
            models.UniqueConstraint(
                name="unique_player_scoring_category_table",
                fields=["player", "scoring_category", "table"],
            )
        ]

    def save(self, *args, **kwargs):
        # Validate that the scoring category belongs to the same game
        # as the table game being played, otherwise it's wrong.
        if self.scoring_category.game != self.table.game:
            raise ValueError("Scoring category must belong to the game.")
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.table.pk} - "
            f"{self.table.game.name} - "
            f"{self.player.user.username} - "
            f"{self.scoring_category.name} - "
            f"{self.value}"
        )
