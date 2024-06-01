from .mock_data import games, tables, user_data, user_profiles


def get_user_profile(username: str) -> dict | None:
    """Get user profile data."""
    return user_profiles.get(username)


def get_user_tables(username: str) -> list[dict]:
    """Get tables where user is a player."""

    def calc_total_scores(scores):
        return sum(scores.values())

    data = user_data.get(username, {})
    user_tables_ids = data.get("tables", [])

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
