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
        "complexity": "4",
        "description": "Agricola is a Euro-style board game created by Uwe Rosenberg. It is a worker placement game with a focus on resource management.",  # noqa E501
        "genres": ["family", "strategy", "euro", "worker placement"],
        "image": "https://cf.geekdo-images.com/dDDo2Hexl80ucK1IlqTk-g__imagepage/img/TLgJgsf7CyGgl8RM2duUYOrE41E=/fit-in/900x600/filters:no_upscale():strip_icc()/pic831744.jpg",  # noqa E501
        "scoring_categories": [
            "victory points",
            "resources",
            "buildings",
            "fields",
            "pastures",
            "grain",
            "vegetables",
            "sheep",
            "wild boar",
            "cattle",
            "unused spaces",
            "fenced stables",
            "rooms",
            "family members",
            "card points",
        ],
    },
    "catan": {
        "name": "Catan",
        "min_players": 3,
        "max_players": 4,
        "min_playtime": 60,
        "max_playtime": 120,
        "complexity": "2",
        "description": "Catan is a Euro-style board game created by Klaus Teuber. It is a resource management game with a focus on trading.",  # noqa E501
        "genres": ["family", "strategy", "euro", "trading"],
        "image": "https://cf.geekdo-images.com/W3Bsga_uLP9kO91gZ7H8yw__imagepage/img/M_3Vg1j2HlNgkv7PL2xl2BJE2bw=/fit-in/900x600/filters:no_upscale():strip_icc()/pic2419375.jpg",  # noqa E501
        "scoring_categories": [
            "towns",
            "cities",
            "longest road",
            "largest army",
            "victory points",
        ],
    },
}

# Tables are games instances played by a group of users. Each table has info about a
# finished game (ongoing games not supported yet).
tables = {
    "table_1": {
        "game": "agricola",
        "players": ["admin", "player1", "player2"],
        "winner": "admin",
        "start_date": "2021-10-01",
        "duration": "1h 30m",
        "scores": {
            "admin": {
                "victory points": 30,
                "resources": 20,
                "buildings": 10,
                "fields": 5,
                "pastures": 5,
                "grain": 5,
                "vegetables": 5,
                "sheep": 5,
                "wild boar": 5,
                "cattle": 5,
                "unused spaces": 5,
                "fenced stables": 5,
                "rooms": 5,
                "family members": 5,
                "card points": 5,
            },
            "player1": {
                "victory points": 20,
                "resources": 10,
                "buildings": 5,
                "fields": 5,
                "pastures": 5,
                "grain": 5,
                "vegetables": 5,
                "sheep": 5,
                "wild boar": 5,
                "cattle": 5,
                "unused spaces": 5,
                "fenced stables": 5,
                "rooms": 5,
                "family members": 5,
                "card points": 5,
            },
            "player2": {
                "victory points": 10,
                "resources": 5,
                "buildings": 5,
                "fields": 5,
                "pastures": 5,
                "grain": 5,
                "vegetables": 5,
                "sheep": 5,
                "wild boar": 5,
                "cattle": 5,
                "unused spaces": 5,
                "fenced stables": 5,
                "rooms": 5,
                "family members": 5,
                "card points": 5,
            },
        },
    },
    "table_2": {
        "game": "catan",
        "players": ["admin", "player3", "player2"],
        "winner": "player2",
        "start_date": "2021-10-02",
        "duration": "1h 10m",
        "scores": {
            "admin": {
                "towns": 4,
                "cities": 2,
                "longest road": 0,
                "largest army": 2,
                "victory points": 8,
            },
            "player3": {
                "towns": 3,
                "cities": 2,
                "longest road": 0,
                "largest army": 0,
                "victory points": 5,
            },
            "player2": {
                "towns": 4,
                "cities": 2,
                "longest road": 2,
                "largest army": 0,
                "victory points": 3,
            },
        },
    },
}
