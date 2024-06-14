from django.db import models

from .ot_player import OTPlayer
from .player import Player
from .scoring_category import ScoringCategory
from .table import Table


class Score(models.Model):
    """Model representing a score for a player, table, scoring category.

    The score can belong either to a registered player (simply `player`)
    or to a one-time player `ot_player` that is not registered in the
    system.

    Attributes:
        - value: The value of the score.
    Relationships:
        - player (many to one)
        - ot_player (many to one)
        - scoring_category (many to one)
        - table (many to one)

    Validation:
        - It's important to check that the scoring category belongs to
        the game that the table is for.
    """

    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="scores")
    player = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name="scores",
        null=True,
        blank=True,
    )
    ot_player = models.ForeignKey(
        OTPlayer,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
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
            ),
        ]

    def clean(self):
        self.validate_game_is_table_game()
        self.validate_player_or_ot_player()

    def validate_game_is_table_game(self):
        """Check that the scoring category belongs to the same game as the table."""
        if self.scoring_category.game != self.table.game:
            raise ValueError("Scoring category must belong to the game.")

    def validate_player_or_ot_player(self):
        """Check that one, and only one, of player or ot_player is set."""
        if self.player is None and self.ot_player is None:
            raise ValueError("player or ot_player must be set.")
        if self.player is not None and self.ot_player is not None:
            raise ValueError("Only one of player or ot_player can be set.")

    def __str__(self):
        return (
            f"{self.table.pk} - "
            f"{self.table.game.name} - "
            f"{self.player.user.username} - "
            f"{self.scoring_category.name} - "
            f"{self.value}"
        )
