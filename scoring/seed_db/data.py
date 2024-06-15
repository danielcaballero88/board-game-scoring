"""Mock data simulating a db for development purposes."""

# Players are users in the scoring context. Other user data is already
# stored in the DB in the account app tables. But that data is related
# to auth. Profiles data is more about user preferences (e.g. favorite
# games, favorite genres, languages they speak, elo score for each game,
# etc.)
players = {
    "admin": {
        "favorite_games": ["agricola", "catan"],
    },
    "player1": {
        "favorite_games": ["agricola"],
    },
    "player2": {
        "favorite_games": ["agricola", "catan"],
    },
    "player3": {
        "favorite_games": ["catan"],
    },
}

# Games are board games that users can play. Each game has info about
# the game in general like min and max players, playtime, complexity,
# genres, etc. It also has a list of scoring categories that can be used
# to score a game. E.g. 'victory points', 'resources', etc...
games = {
    "agricola": {
        "name": "Agricola",
        "min_players": 1,
        "max_players": 5,
        "min_playtime": 30,
        "max_playtime": 150,
        "complexity": 4,
        "description": "Agricola is a Euro-style board game created by Uwe Rosenberg. It is a worker placement game with a focus on resource management.",  # noqa E501
        "genres": ["Family", "Strategy", "Euro", "Worker placement"],
        "image": "https://cf.geekdo-images.com/dDDo2Hexl80ucK1IlqTk-g__imagepage/img/TLgJgsf7CyGgl8RM2duUYOrE41E=/fit-in/900x600/filters:no_upscale():strip_icc()/pic831744.jpg",  # noqa E501
        "scoring_categories": [
            "Victory points",
            "Resources",
            "Buildings",
            "Fields",
            "Pastures",
            "Grain",
            "Vegetables",
            "Sheep",
            "Wild boar",
            "Cattle",
            "Unused spaces",
            "Fenced stables",
            "Rooms",
            "Family members",
            "Card points",
        ],
    },
    "catan": {
        "name": "Catan",
        "min_players": 3,
        "max_players": 4,
        "min_playtime": 60,
        "max_playtime": 120,
        "complexity": 2,
        "description": "Catan is a Euro-style board game created by Klaus Teuber. It is a resource management game with a focus on trading.",  # noqa E501
        "genres": ["Family", "Strategy", "Euro", "Trading"],
        "image": "https://cf.geekdo-images.com/W3Bsga_uLP9kO91gZ7H8yw__imagepage/img/M_3Vg1j2HlNgkv7PL2xl2BJE2bw=/fit-in/900x600/filters:no_upscale():strip_icc()/pic2419375.jpg",  # noqa E501
        "scoring_categories": [
            "Towns",
            "Cities",
            "Longest road",
            "Largest army",
            "Victory points",
        ],
    },
}

# Tables are games instances played by a group of users. Each table has info about a
# finished game (ongoing games not supported yet).
tables = {
    "table_1": {
        # Unlike other models, different tables can be created with the
        # same set of values, so I set an id to make the seed_db script
        # idempotent.
        "id": 1,
        "game": "Agricola",
        "players": ["admin", "player1", "player2"],
        "ot_players": [],  # one time players
        "owner": "admin",
        "start_date": "2021-10-01",
        "closed": True,
        "scores": {
            "players": {
                "admin": {
                    "Victory points": 30,
                    "Resources": 20,
                    "Buildings": 10,
                    "Fields": 5,
                    "Pastures": 5,
                    "Grain": 5,
                    "Vegetables": 5,
                    "Sheep": 5,
                    "Wild boar": 5,
                    "Cattle": 5,
                    "Unused spaces": 5,
                    "Fenced stables": 5,
                    "Rooms": 5,
                    "Family members": 5,
                    "Card points": 5,
                },
                "player1": {
                    "Victory points": 20,
                    "Resources": 10,
                    "Buildings": 5,
                    "Fields": 5,
                    "Pastures": 5,
                    "Grain": 5,
                    "Vegetables": 5,
                    "Sheep": 5,
                    "Wild boar": 5,
                    "Cattle": 5,
                    "Unused spaces": 5,
                    "Fenced stables": 5,
                    "Rooms": 5,
                    "Family members": 5,
                    "Card points": 5,
                },
                "player2": {
                    "Victory points": 10,
                    "Resources": 5,
                    "Buildings": 5,
                    "Fields": 5,
                    "Pastures": 5,
                    "Grain": 5,
                    "Vegetables": 5,
                    "Sheep": 5,
                    "Wild boar": 5,
                    "Cattle": 5,
                    "Unused spaces": 5,
                    "Fenced stables": 5,
                    "Rooms": 5,
                    "Family members": 5,
                    "Card points": 5,
                },
            },
            "ot_players": {},
        },
    },
    "table_2": {
        # Unlike other models, different tables can be created with the
        # same set of values, so I set an id to make the seed_db script
        # idempotent.
        "id": 2,
        "game": "Catan",
        "players": ["admin", "player3", "player2"],
        "ot_players": ["ot_player_1"],  # one time players
        "owner": "admin",
        "start_date": "2021-10-02",
        "closed": True,
        "scores": {
            "players": {
                "admin": {
                    "Towns": 4,
                    "Cities": 2,
                    "Longest road": 0,
                    "Largest army": 2,
                    "Victory points": 8,
                },
                "player3": {
                    "Towns": 3,
                    "Cities": 2,
                    "Longest road": 0,
                    "Largest army": 0,
                    "Victory points": 5,
                },
                "player2": {
                    "Towns": 4,
                    "Cities": 2,
                    "Longest road": 2,
                    "Largest army": 0,
                    "Victory points": 3,
                },
            },
            "ot_players": {
                "ot_player_1": {
                    "Towns": 2,
                    "Cities": 2,
                    "Longest road": 0,
                    "Largest army": 0,
                    "Victory points": 3,
                },
            },
        },
    },
    "table_3": {
        # Unlike other models, different tables can be created with the
        # same set of values, so I set an id to make the seed_db script
        # idempotent.
        "id": 3,
        "game": "Catan",
        "players": ["admin", "player1"],
        "ot_players": ["ot_player_x"],  # one time players
        "owner": "admin",
        "start_date": "2021-10-03",
        "closed": False,
        "scores": {
            "players": {
                "admin": {
                    "Towns": 4,
                    "Cities": 2,
                    "Longest road": 0,
                    "Largest army": 2,
                    "Victory points": 2,
                },
            },
            "ot_players": {},
        },
    },
}
