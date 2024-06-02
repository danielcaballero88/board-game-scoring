from .mock_data import games, players, tables


def get_player_obj(username: str) -> dict | None:
    """Get user profile data."""
    return players.get(username)


def get_user_tables(username: str) -> list[dict]:
    """Get tables where user is a player."""

    def calc_total_scores(scores):
        return sum(scores.values())

    player_obj = players.get(username, {})
    user_tables_ids = player_obj.get("tables", [])

    user_tables = []
    for user_table_id in user_tables_ids:
        table = {}
        table_db = tables.get(user_table_id)
        table["game"] = games[table_db["game"]]["name"]
        table["winner"] = table_db["winner"]
        table["date"] = table_db["start_date"]
        table["total_scores"] = {}
        for playername in table_db["scores"]:
            table["total_scores"][playername] = calc_total_scores(
                table_db["scores"][playername]
            )
        user_tables.append(table)

    return user_tables


def get_favorite_games(username: str) -> list[dict]:
    """Get favorite games of a user."""
    player_obj = get_player_obj(username)
    if not player_obj:
        return []

    fav_games_ids = player_obj.get("favorite_games", [])

    fav_games = []
    for game_id in fav_games_ids:
        game_obj = games.get(game_id)
        table_objs = [
            tables[table_id]
            for table_id in player_obj.get("tables", [])
            if tables[table_id]["game"] == game_id
        ]
        fav_game = {}
        fav_game["name"] = game_obj["name"]
        fav_game["description"] = game_obj["description"]
        fav_game["img_src"] = game_obj["image"]
        fav_game["record"] = {
            "total_played": len(table_objs),
            "total_won": len(
                [table for table in table_objs if table["winner"] == username]
            ),
        }
        fav_games.append(fav_game)

    return fav_games
