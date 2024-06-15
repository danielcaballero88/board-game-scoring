from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import models

from .game import Game

if TYPE_CHECKING:
    from .score import Score
    from .table import Table

User = get_user_model()


class Player(models.Model):
    """Model representing a player.

    Relationships:
        - user (one to one): Auth user object.
        - favorite_games (many to many)
        - tables (many to many)
    """

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    favorite_games = models.ManyToManyField(Game)

    @classmethod
    def get_by_username(cls, username: str) -> Player:
        return cls.objects.get(user__username=username)

    @property
    def name(self) -> str:
        return self.user.username

    def get_favorite_games(self) -> list[Game]:
        return self.favorite_games.all()

    def get_scores_by_table(self, table: Table) -> list[Score]:
        return self.scores.filter(table=table)

    def get_record(self, game: Game) -> dict[str, int]:
        tables_game = self.tables.filter(game=game)
        tables_played_count = tables_game.count()
        # TODO: This can be optimized by using a query, but to do that
        # I need to have a field `winner` in the table. The problem now
        # is that the winner could be either a Player or an OTPlayer.
        # So I need to implement a relation manually by storing two
        # values, one for the type of player and one for the id.
        # Doable but I don't want to spend time on it now.
        tables_won_count = 0
        for table in tables_game:
            if table.winner == self:
                tables_won_count += 1
        return {"won": tables_won_count, "played": tables_played_count}

    def get_tables(self) -> list[Table]:
        return self.tables.all()

    def add_fav_game(self, game: Game):
        self.favorite_games.add(game)

    def remove_fav_game(self, game: Game):
        self.favorite_games.remove(game)

    def __str__(self):
        return f"{self.user.username}"
