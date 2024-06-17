from .game import Game
from .genre import Genre
from .ot_player import OTPlayer
from .player import Player
from .score import Score
from .scoring_category import ScoringCategory
from .table import Table


def get_player_or_ot_player(table: Table, playername: str):
    player = None
    try:
        player = table.players.get(user__username=playername)
    except Player.DoesNotExist:
        try:
            player = table.ot_players.get(name=playername)
        except OTPlayer.DoesNotExist:
            raise ValueError(f"Player {playername} not found in table {table}")
    return player
