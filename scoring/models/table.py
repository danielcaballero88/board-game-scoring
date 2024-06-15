from django.contrib.auth import get_user_model
from django.db import models

from .game import Game
from .player import Player

User = get_user_model()


class Table(models.Model):
    """Model representing a table (an instance of a game).

    A table can be created by a user and they can then share a link with
    other users and also with non-users. Users will be added as
    `players` and non-users as `ot_players`.
    TODO: maybe I can unify players by automatically registering
    non-users with the username they provide. Not sure if it's the best
    approach because it requires that the username be unique, so it may
    take longer for one-time players to enter a score, which would be
    bad ux.

    After creation a table has status `open` and admits new players
    which got the link to submit new scores for it. The owner can close
    the table at any time. They can see the players that have already
    submitted scores so they should know when everybody has done their
    part.

    When the owner closes the table, the winner is calculated and the
    table is marked as `closed`.

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
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=10,
        choices=[("open", "Open"), ("closed", "Closed")],
        default="open",
    )
    start_date = models.DateField()
    players = models.ManyToManyField(Player, related_name="tables")
    winner = models.ForeignKey(
        Player,
        related_name="tables_won",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def close(self):
        self.status = "closed"
        self.save()

    def clean(self):
        self.validate_unique_names()

    def validate_unique_names(self):
        player_names = [player.user.username for player in self.players.all()]
        ot_player_names = [player.name for player in self.ot_players.all()]
        names = player_names + ot_player_names
        if len(names) != len(set(names)):
            raise ValueError("Players must have unique names.")

    def __str__(self):
        return (
            f"{self.game.name} - "
            f"{self.start_date} - "
            f"owner: {self.owner.username}"
        )
