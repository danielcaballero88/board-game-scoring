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

    name = models.CharField(max_length=100)
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

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    game = models.ForeignKey(  # many-to-one relationship
        Game, on_delete=models.CASCADE, related_name="scoring_category_set"
    )

    def __str__(self):
        return self.name


class Player(models.Model):
    """Model representing a player.

    Attributes:
        - nickname: Name shown for gaming purposes.
    Relationships:
        - user (one to one): Auth user object.
        - favorite_game_set (many to many)
        - table_set (many to many)
        - table_winner_set (one to many)
    """

    nickname = models.CharField(max_length=100, unique=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    favorite_games = models.ManyToManyField(Game)

    @property
    def is_registered(self):
        return self.user.username if self.user else ""

    def __str__(self):
        return f"{self.nickname} ({self.is_registered})"


class Table(models.Model):
    """Model representing a table (an instance of a game).

    Attributes:
        - name: The name of the table.
    Relationships:
        - game (many to one): The game that the table is for.
        - player_set (many to many): The players at the table.
        - winner (many to one): The winning player.
    """

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player)
    winner = models.ForeignKey(
        Player, related_name="table_winner_set", on_delete=models.PROTECT
    )
    start_date = models.DateField()
    duration = models.IntegerField("Duration in minutes")

    def __str__(self):
        return (
            f"{self.game.name} - "
            f"{self.start_date} - "
            f"{[player.nickname for player in self.players.all()]}"
        )


class Score(models.Model):
    """Model representing a score for a player, table, scoring category.

    Attributes:
        - value: The value of the score.
    Relationships:
        - player (many to one)
        - scoring_category (many to one)
        - table (many to one)
    """

    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    scoring_category = models.ForeignKey(ScoringCategory, on_delete=models.PROTECT)
    value = models.IntegerField()

    def __str__(self):
        return (
            f"{self.table.game.name} - "
            f"{self.player.nickname} - "
            f"{self.scoring_category.name} - "
            f"{self.value}"
        )
