from .data import games


def get_game_slug(game_name: str) -> str:
    return game_name.replace(" ", "-").lower()


def get_game(game_slug: str) -> dict | None:
    """Get game data."""
    return games.get(game_slug)
