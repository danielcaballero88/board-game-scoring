from django.db import models


class Genre(models.Model):
    """Model representing a board game genre.

    Attributes:
        - name: Genre name.
    Relationships:
        - games (many to many)
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
