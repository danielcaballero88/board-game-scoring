# Scoring App

## Models

### Games

Here games are "game classes". For instance the game "Agricola" is the game itself, not a particular instance or match being played or having been played.

Relatioinships:

- The main model is, of course, `Game`.
- A many to many relationship exists with the model `Genre`
- A one to many relationship exists with the model `ScoringCategory`
  - Each game has a number of scoring categories that belong to that game only and that are used to score at the end of the game.

### Players

The `Player` model represents a `User`. The difference is that `User` is the authentication model provided by the `accounts` app but the `Player` model holds
the data necessary for the `scoring` app to function properly.

### Table

This is an instance of a game being played or having been played.

- It has an `owner` which is a `Player`.
- It has a `winner` which is a `Player`.
- It has a `players` which is a set of `Player` at the table, including the `owner` and the `winner`.
- It has a `scores` which is a list of scores.
  - The score model is `Score` which represents a score for a single player, at a single table, for a single scoring category. Besides these relationships it has a single integer field: `value`.

TODO:

- Allow more than one winner for games that end in ties.
  - Note that now winners are calculated on the fly and not a field in Table anymore so it's easier to implement ties, because winner is a propery method in the Table class.
- There is a bit of code duplication between `score_create_ot_player` and `score_edit` (and now also `score_create_self`), so it can maybe be improved, but it's not critical either.
- Add custom 403 page that allows the user to go back to their previous page, similar for 404 and others maybe? Maybe a general error page and some specific error pages.
