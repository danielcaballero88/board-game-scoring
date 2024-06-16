from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .genre import Genre

if TYPE_CHECKING:
    from .scoring_category import ScoringCategory
    from .table import Table


class Game(models.Model):
    """Model representing a board game.

    Attributes:
        - name: The name of the game.
        - min_players: The minimum number of players.
        - max_players: The maximum number of players.
        - min_playtime: The minimum number of minutes for a match.
        - max_playtime: The maximum number of minutes for a match.
        - complexity: A rating of the complexity from 1 to 5.
        - description: A description of the game.
        - image: A URL to an image of the game.
    Relationships:
        - genres: (many to many): Genres that the game belongs to.
        - scoring_categories (one to many): A list of scoring
          categories that can be used to score the game.
        - tables (one to many): Tables that played this game.
    """

    name = models.CharField(max_length=100, unique=True)
    min_players = models.IntegerField(blank=True, null=True)
    max_players = models.IntegerField(blank=True, null=True)
    min_playtime = models.IntegerField(blank=True, null=True)
    max_playtime = models.IntegerField(blank=True, null=True)
    complexity = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )
    description = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre, related_name="games")
    image = models.URLField(blank=True)

    # These type hints are not entirely correct, the right type is
    # RelatedManager[T] but this type is generated at runtime and is not
    # available during static type checking. Also, this is good enough
    # to get good autocomplete for `get`, `filter`, etc.
    scoring_categories: models.QuerySet[ScoringCategory]
    tables: models.QuerySet[Table]

    def __str__(self):
        return self.name
