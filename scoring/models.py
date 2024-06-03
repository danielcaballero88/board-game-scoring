from django.contrib.auth import get_user_model
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
    min_players = models.IntegerField(null=True)
    max_players = models.IntegerField(null=True)
    min_playtime = models.IntegerField(null=True)
    max_playtime = models.IntegerField(null=True)
    complexity = models.CharField(max_length=1, null=True)
    description = models.TextField(null=True)
    genres = models.ManyToManyField(Genre)
    image = models.URLField(null=True)


class ScoringCategory(models.Model):
    """Model representing a scoring category.

    Attributes:
        - name: The name of the scoring category.
        - description: A description of the scoring category.
    Relationships:
        - game (many to one): The game that the scoring category belongs to.
    """

    name = models.CharField(max_length=100)
    description = models.TextField()
    game = models.ForeignKey(  # many-to-one relationship
        Game, on_delete=models.CASCADE, related_name="scoring_category_set"
    )


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

    nickname = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    favorite_games = models.ManyToManyField(Game)


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
