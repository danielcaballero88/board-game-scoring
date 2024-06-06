"""Script to seed the DB with scoring data.

Usage:
$ python manage.py shell < $PATH_TO_THIS_SCRIPT
"""

from django.contrib.auth import get_user_model
from django.db import IntegrityError

# It's important to use absolute imports because this will be run as a
# script from root directory from inside Django shell.
from scoring.models import Game, Genre, Player, Score, ScoringCategory, Table
from scoring.seed_db.data import games, players, tables

User = get_user_model()


def insert_genre(genre_name: str) -> Genre:
    try:
        print("Inserting genre into DB:", genre_name)
        genre_obj, _ = Genre.objects.get_or_create(name=genre_name)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error creating genre: {exc}")
        raise exc
    else:
        return genre_obj


def insert_game(game_dict: dict) -> Game:
    # Create the game object
    try:
        print("Inserting game into DB:", game_dict["name"])
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
    except IntegrityError as exc:
        if "unique constraint" in exc.args[0].lower():
            print(f"Game already exists in DB: {game_dict['name']}")
            game_obj = Game.objects.get(name=game_dict["name"])
        else:
            raise exc
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error creating game: {exc}")
        raise exc

    return game_obj


def add_genre_to_game(game_obj: Game, genre_obj: Genre) -> None:
    try:
        print("Adding genre to game:", genre_obj, game_obj)
        game_obj.genres.add(genre_obj)
    except IntegrityError as exc:
        if "unique constraint" in exc.args[0].lower():
            print(f"Genre-game relationship already exists in DB: {genre_obj.name}")
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error creating genre: {exc}")
        raise exc


def insert_scoring_category(game_obj: Game, category_name: str) -> None:
    try:
        print("Inserting scoring category into DB:", category_name)
        game_obj.scoring_category_set.create(name=category_name)
    except IntegrityError as exc:
        if "unique constraint" in exc.args[0].lower():
            print(
                f"Scoring category already exists in DB: {game_obj.name, category_name}"
            )
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error creating scoring category: {exc}")
        raise exc


def insert_games():
    for game_dict in games.values():
        # Create the game object
        game_obj = insert_game(game_dict)

        # Genres need to be created separately and then linked together.
        # It's possible that a genre already exists in the DB, so we need to
        # check for that.
        # Note that it's a many to many relationship.
        genres = game_dict["genres"]
        for genre_name in genres:
            genre_obj = insert_genre(genre_name)
            add_genre_to_game(game_obj, genre_obj)

        # Scoring categories should be added to the game, it's a one to
        # many relationship.
        scoring_categories = game_dict["scoring_categories"]
        for category_name in scoring_categories:
            insert_scoring_category(game_obj, category_name)


def insert_player(username: str) -> Player:
    # The user should exist already in the DB.
    user_obj = User.objects.get(username=username)

    try:
        print("Inserting player into DB:", username)
        player_obj = Player.objects.create(user=user_obj)
    except IntegrityError as exc:
        if "unique constraint" in exc.args[0].lower():
            print(f"Player already exists in DB: {username}")
            player_obj = Player.objects.get(user__username=username)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error creating player: {exc}")
        raise exc
    else:
        return player_obj


def add_player_favorite_game(player_obj: Player, game_obj: Game) -> None:
    try:
        print(
            "Adding favorite game to player:", game_obj.name, player_obj.user.username
        )
        player_obj.favorite_games.add(game_obj)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error adding favorite game to player: {exc}")


def insert_players():
    for username, player_dict in players.items():
        player_obj = insert_player(username)

        for game_slug in player_dict["favorite_games"]:
            game_obj = Game.objects.get(name=games[game_slug]["name"])
            add_player_favorite_game(player_obj, game_obj)


def insert_tables():
    for table_dict in tables:
        try:
            print("Inserting table into DB:", table_dict["name"])
            table_obj = Table.objects.create(
                name=table_dict["name"],
                game=Game.objects.get(name=table_dict["game"]),
            )
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Error creating table: {exc}")

        for player_username in table_dict["players"]:
            player_obj = Player.objects.get(user__username=player_username)
            try:
                print("Adding player to table:", player_username, table_dict["name"])
                table_obj.players.add(player_obj)
            except Exception as exc:  # pylint: disable=broad-except
                print(f"Error adding player to table: {exc}")

        for username, score_dict in table_dict["scores"].items():
            player_obj = Player.objects.get(user__username=username)
            try:
                print(
                    "Inserting score into DB:", score_dict["player"], table_dict["name"]
                )
                score_obj = Score.objects.create(
                    player=player_obj,
                    table=table_obj,
                )
            except Exception as exc:  # pylint: disable=broad-except
                print(f"Error creating score: {exc}")

            for category_name, value in score_dict["scores"].items():
                category_obj = ScoringCategory.objects.get(
                    game=table_obj.game, name=category_name
                )
                try:
                    print("Inserting score value into DB:", category_name, value)
                    score_obj.scores.create(
                        category=category_obj,
                        value=value,
                    )
                except Exception as exc:  # pylint: disable=broad-except
                    print(f"Error creating score value: {exc}")


try:
    insert_games()
except Exception as exc:  # pylint: disable=broad-except
    print(f"Aborted: {dir(exc)}")
    print(type(exc))
    print(exc.args[0])
