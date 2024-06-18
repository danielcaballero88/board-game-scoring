from django.db import models

from .game import Game


class ScoringCategory(models.Model):
    """Model representing a scoring category.

    Attributes:
        - name: The name of the scoring category.
        - description: A description of the scoring category.
    Relationships:
        - game (many to one): The game that owns this category.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    game = models.ForeignKey(  # many-to-one relationship
        Game, on_delete=models.CASCADE, related_name="scoring_categories"
    )

    class Meta:
        # Each game should have only one scoring category with the same name.
        constraints = [
            models.UniqueConstraint(
                name="unique_scoring_category_name_per_game",
                fields=["name", "game"],
            )
        ]

    @property
    def safe_string(self):
        return self.name.replace(" ", "_").lower()

    def __str__(self):
        return self.name
