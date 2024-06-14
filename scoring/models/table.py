from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from .game import Game
from .player import Player

User = get_user_model()


class Table(models.Model):
    """Model representing a table (an instance of a game).

    Attributes:
        - name: The name of the table.
    Relationships:
        - game (many to one): The game that the table is for.
        - owner (many to one): The user that created the table.
        - winner (many to one): The winning player.
        - players (many to many): The players at the table, including
          the owner and the winner.
        - ot_players (one to many): The one-time players at the table.
        - scores (one to many): The scores for the table.
    """

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="tables")
    players = models.ManyToManyField(Player, related_name="tables")
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    winner = models.ForeignKey(
        Player,
        related_name="tables_won",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    start_date = models.DateField()
    duration = models.IntegerField(
        "Duration in minutes", null=True, blank=True, validators=[MinValueValidator(0)]
    )

    def save(self):
        self.validate_unique_names()

    def validate_unique_names(self):
        names = [player.username.name for player in self.players.all()]
        names += [player.name for player in self.ot_players.all()]
        if len(names) != len(set(names)):
            raise ValueError("Players must have unique names.")

    def __str__(self):
        return (
            f"{self.game.name} - "
            f"{self.start_date} - "
            f"owner: {self.owner.username}"
        )
