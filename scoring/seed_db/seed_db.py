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
        genre_obj, created = Genre.objects.get_or_create(name=genre_name)
        if not created:
            print("  Genre already exists in DB:", genre_name)
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
            print(f"  Game already exists in DB: {game_dict['name']}")
            game_obj = Game.objects.get(name=game_dict["name"])
        else:
            raise exc
    except Exception as exc:  # pylint: disable=broad-except
        print(f"  Error creating game: {exc}")
        raise exc

    return game_obj


def add_genre_to_game(game_obj: Game, genre_obj: Genre) -> None:
    try:
        print("Adding genre to game:", genre_obj, game_obj)
        # The .add opperation doesn't raise an exception if the
        # relationship already exists. So we check for the existence
        # beforehand to get a cleaner output.
        if game_obj.genres.filter(name=genre_obj.name).exists():
            print(
                "  Genre-game relationship already exists in DB: "
                f"{game_obj}-{genre_obj}"
            )
            return
        game_obj.genres.add(genre_obj)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"  Error creating genre: {exc}")
        raise exc


def insert_scoring_category(game_obj: Game, category_name: str) -> None:
    try:
        print("Inserting scoring category into DB:", category_name)
        game_obj.scoring_categories.create(name=category_name)
    except IntegrityError as exc:
        if "unique constraint" in exc.args[0].lower():
            print(
                "  Scoring category already exists in DB: "
                f"{game_obj.name, category_name}"
            )
    except Exception as exc:  # pylint: disable=broad-except
        print(f"  Error creating scoring category: {exc}")
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
    try:
        user_obj = User.objects.get(username=username)
        print("Inserting player into DB:", username)
        player_obj = Player.objects.create(user=user_obj)
    except IntegrityError as exc:
        if "unique constraint" in exc.args[0].lower():
            print(f"  Player already exists in DB: {username}")
            player_obj = Player.objects.get(user__username=username)
        else:
            raise exc
    except Exception as exc:  # pylint: disable=broad-except
        print(f"  Error creating player: {username} - {exc}")
        raise exc

    return player_obj


def add_player_favorite_game(player_obj: Player, game_obj: Game) -> None:
    try:
        print(
            "Adding favorite game to player:", game_obj.name, player_obj.user.username
        )
        # The .add opperation doesn't raise an exception if the relation
        # already exists. So we check for the existence beforehand to
        # get a cleaner output.
        if player_obj.favorite_games.filter(name=game_obj.name).exists():
            print(
                "  Favorite game-player relationship already exists in DB: "
                f"{game_obj}-{player_obj}"
            )
            return
        player_obj.favorite_games.add(game_obj)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"  Error adding favorite game to player: {exc}")


def insert_players():
    for username, player_dict in players.items():
        player_obj = insert_player(username)

        for game_slug in player_dict["favorite_games"]:
            game_obj = Game.objects.get(name=games[game_slug]["name"])
            add_player_favorite_game(player_obj, game_obj)


def insert_table(table_dict: dict) -> Table:
    try:
        table_str = (
            f"{table_dict['id']} - "
            f"{table_dict['start_date']} - "
            f"{table_dict['game']} - "
            f"{table_dict['players']}"
        )
        print(f"Inserting table into DB: {table_str}")
        table_obj = Table.objects.create(
            pk=table_dict["id"],
            game=Game.objects.get(name=table_dict["game"]),
            owner=User.objects.get(username=table_dict["owner"]),
            winner=Player.objects.get(user__username=table_dict["winner"]),
            start_date=table_dict["start_date"],
            duration=table_dict["duration"],
        )
    except IntegrityError as exc:
        if "unique constraint" in exc.args[0].lower():
            print(f"  Player already exists in DB: {table_str}")
            table_obj = Table.objects.get(pk=table_dict["id"])
        else:
            raise exc
    except Exception as exc:  # pylint: disable=broad-except
        print(f"  Error creating table: {exc}")
        raise exc

    return table_obj


def add_player_to_table(player_obj: Player, table_obj: Table) -> None:
    try:
        print("Adding player to table:", player_obj, table_obj)
        # The .add opperation doesn't raise an exception if the relation
        # already exists. So we check for the existence beforehand to
        # get a cleaner output.
        if table_obj.players.filter(user__username=player_obj.user.username).exists():
            print(
                "  Player-table relationship already exists in DB: "
                f"{player_obj}-{table_obj}"
            )
            return
        table_obj.players.add(player_obj)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"  Error adding player to table: {exc}")
        raise exc


def insert_score(
    table_obj: Table, player_obj: Player, sc_obj: ScoringCategory, value: int
) -> None:
    try:
        print("Inserting score into DB:", table_obj, player_obj, sc_obj, value)
        Score.objects.create(
            table=table_obj,
            player=player_obj,
            scoring_category=sc_obj,
            value=value,
        )
    except IntegrityError as exc:
        if "unique constraint" in exc.args[0].lower():
            print(
                "  Score already exists in DB: "
                f"{table_obj} - {player_obj} - {sc_obj} - {value}"
            )
        else:
            raise exc
    except Exception as exc:  # pylint: disable=broad-except
        print(
            f"  Error creating score: {table_obj} - {player_obj} - {sc_obj} - {value} -"
            f" {exc}"
        )
        raise exc


def insert_tables():
    for table_dict in tables.values():
        table_obj = insert_table(table_dict)

        for username in table_dict["players"]:
            player_obj = Player.objects.get(user__username=username)
            add_player_to_table(player_obj, table_obj)

        for username, score_dict in table_dict["scores"].items():
            player_obj = Player.objects.get(user__username=username)
            for scoring_category_name, value in score_dict.items():
                sc_obj = ScoringCategory.objects.get(
                    game__name=table_obj.game, name=scoring_category_name
                )
                insert_score(table_obj, player_obj, sc_obj, value)


try:
    insert_games()
    insert_players()
    insert_tables()
except Exception as exc:  # pylint: disable=broad-except
    print(f"Aborted: {dir(exc)}")
    print(type(exc))
    print(exc.args[0])
