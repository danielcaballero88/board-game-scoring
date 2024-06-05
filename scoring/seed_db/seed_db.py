"""Script to seed the DB with scoring data.

Usage:
$ python manage.py shell < $PATH_TO_THIS_SCRIPT
"""

from django.contrib.auth import get_user_model

from ..models import Game, Genre, Player, Score, ScoringCategory, Table
from .data import games, players, tables

User = get_user_model()


# Games go first.
for game_dict in games.values():
    # Create the game object
    game_obj = Game.objects.create(
        name=game_dict["name"],
        min_players=game_dict["min_players"],
        max_players=game_dict["max_players"],
        min_playtime=game_dict["min_playtime"],
        max_playtime=game_dict["max_playtime"],
        complexity=game_dict["complexity"],
        description=game_dict["description"],
        image=game_dict["image"],
    )
    # Genres need to be created separately and then linked together.
    # It's possible that a genre already exists in the DB, so we need to
    # check for that.
    # Note that it's a many to many relationship.
    genres = game_dict["genres"]
    for genre_name in genres:
        genre_obj, _ = Genre.objects.get_or_create(name=genre_name)
        game_obj.genres.add(genre_obj)

    # Scoring categories should be added to the game, it's a one to
    # many relationship.
    scoring_categories = game_dict["scoring_categories"]
    for category_name in scoring_categories:
        game_obj.scoring_category_set.create(name=category_name)


# Players.
for username, player_dict in players.items():
    # The user should exist already in the DB.
    user_obj = User.objects.get(username=username)

    player_obj = Player.objects.create(
        user=user_obj,
    )

    for game_slug in player_dict["favorite_games"]:
        game_obj = Game.objects.get(name=game_slug)
        player_obj.favorite_games.add(game_obj)


# Tables.
for table_dict in tables:
    table_obj = Table.objects.create(
        name=table_dict["name"],
        game=Game.objects.get(name=table_dict["game"]),
    )

    for player_username in table_dict["players"]:
        player_obj = Player.objects.get(user__username=player_username)
        table_obj.players.add(player_obj)

    for score_dict in table_dict["scores"]:
        player_obj = Player.objects.get(user__username=score_dict["player"])
        score_obj = Score.objects.create(
            player=player_obj,
            table=table_obj,
        )
        for category_name, value in score_dict["scores"].items():
            category_obj = ScoringCategory.objects.get(
                game=table_obj.game, name=category_name
            )
            score_obj.scores.create(
                category=category_obj,
                value=value,
            )
