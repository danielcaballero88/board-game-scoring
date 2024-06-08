from django.contrib.auth import get_user_model
from django.db import models

from .game import Game

User = get_user_model()


class Player(models.Model):
    """Model representing a player.

    Relationships:
        - user (one to one): Auth user object.
        - favorite_games (many to many)
        - tables (many to many)
        - tables_won (one to many)
    """

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    favorite_games = models.ManyToManyField(Game)

    def __str__(self):
        return f"{self.user.username}"
