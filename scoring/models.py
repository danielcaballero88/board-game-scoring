from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Genre(models.Model):
    """Model representing a board game genre.

    Attributes:
        - name: Genre name.
    Relationships:
        - game_set (many to many)
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


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
        - genre_set: (many to many): Genres that the game belongs to.
        - scoring_category_set (one to many): A list of scoring
          categories that can be used to score the game.
        - table_set (one to many): Tables that played this game.
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
    genres = models.ManyToManyField(Genre)
    image = models.URLField(blank=True)

    def __str__(self):
        return self.name


class ScoringCategory(models.Model):
    """Model representing a scoring category.

    Attributes:
        - name: The name of the scoring category.
        - description: A description of the scoring category.
    Relationships:
        - game (many to one): The game that the scoring category belongs to.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    game = models.ForeignKey(  # many-to-one relationship
        Game, on_delete=models.CASCADE, related_name="scoring_category_set"
    )

    class Meta:
        # Each game should have only one scoring category with the same name.
        constraints = [
            models.UniqueConstraint(
                name="unique_scoring_category_name_per_game",
                fields=["name", "game"],
            )
        ]

    def __str__(self):
        return self.name


class Player(models.Model):
    """Model representing a player.

    Relationships:
        - user (one to one): Auth user object.
        - favorite_games (many to many)
        - table_set (many to many)
        - table_winner_set (one to many)
    """

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    favorite_games = models.ManyToManyField(Game)

    def __str__(self):
        return f"{self.user.username}"


class Table(models.Model):
    """Model representing a table (an instance of a game).

    Attributes:
        - name: The name of the table.
    Relationships:
        - game (many to one): The game that the table is for.
        - owner (many to one): The user that created the table.
        - winner (many to one): The winning player.
        - player_set (many to many): The players at the table, including
          the owner and the winner.
        - score_set (one to many): The scores for the table.
    """

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    winner = models.ForeignKey(
        Player,
        related_name="table_winner_set",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    start_date = models.DateField()
    duration = models.IntegerField(
        "Duration in minutes", null=True, blank=True, validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return (
            f"{self.game.name} - "
            f"{self.start_date} - "
            f"{[player.user.username for player in self.players.all()]}"
        )


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

    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    scoring_category = models.ForeignKey(ScoringCategory, on_delete=models.PROTECT)
    value = models.IntegerField()

    def save(self, *args, **kwargs):
        # Validate that the scoring category belongs to the same game
        # as the table game being played, otherwise it's wrong.
        if self.scoring_category.game != self.table.game:
            raise ValueError("Scoring category must belong to the game.")
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.table.game.name} - "
            f"{self.player.user.username} - "
            f"{self.scoring_category.name} - "
            f"{self.value}"
        )
