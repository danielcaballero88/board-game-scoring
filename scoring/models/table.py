from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import models

from .game import Game
from .player import Player

if TYPE_CHECKING:
    from .ot_player import OTPlayer
    from .score import Score

User = get_user_model()


class Table(models.Model):
    """Model representing a table (an instance of a game).

    A table can be created by a user and they can then share a link with
    other users and also with non-users. Users will be added as
    `players` and non-users as `ot_players`.
    IDEA: maybe I can unify players by automatically registering
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

    # One-time players (backwards relation). The type is not entirely
    # correct because the actual type is `RelatedManager` but that is
    # set during runtime. This is good enough for type checking.
    ot_players: models.QuerySet[OTPlayer]

    def close(self) -> None:
        self.status = "closed"
        self.save()

    def open(self) -> None:
        self.status = "open"
        self.save()

    @property
    def scores_dict(self) -> dict[Player | OTPlayer, Score]:
        result = {}
        for player in itertools.chain(self.players.all(), self.ot_players.all()):
            player_scores = player.get_scores_by_table(self)
            result[player] = player_scores
        return result

    @property
    def totals_dict(self) -> dict[Player | OTPlayer, int]:
        totals = {}
        for player, score in self.scores_dict.items():
            player_scores = player.get_scores_by_table(self)
            totals[player] = sum(player_scores.values_list("value", flat=True))
        return totals

    @property
    def winner(self) -> Player | OTPlayer | None:
        if self.status != "closed":
            return None
        winner = None
        winner_total_score = -9999
        for player, total in self.totals_dict.items():
            if total > winner_total_score:
                winner = player
                winner_total_score = total
        return winner

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
            f"owner: {self.owner.username} - "
            f"status: {self.status} - "
        )
